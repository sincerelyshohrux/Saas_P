"""Excel (.xlsx) va CSV importi. Katta fayllar uchun bulk_create / bulk_update ishlatiladi."""
import io
import logging

import pandas as pd
from django.db import transaction
from django.utils import timezone

from apps.catalog.models import ImportJob, Product
from .validators import REQUIRED, map_columns, clean_text, validate_row

logger = logging.getLogger(__name__)

MAX_ROWS = 100_000
MAX_ERRORS_STORED = 10_000
LOOKUP_CHUNK = 5_000


class ImportFileError(Exception):
    """Foydalanuvchiga ko'rsatish mumkin bo'lgan xato."""


def _read_csv(data: bytes) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "cp1251"):
        try:
            text = data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ImportFileError("CSV kodirovkasi tanilmadi (UTF-8 yoki Windows-1251 bo'lishi kerak).")
    return pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False, sep=None, engine="python")


def read_table(job: ImportJob) -> pd.DataFrame:
    name = job.original_name.lower()
    job.file.open("rb")
    try:
        data = job.file.read()
    finally:
        job.file.close()
    try:
        if name.endswith(".xlsx"):
            return pd.read_excel(io.BytesIO(data), dtype=str, keep_default_na=False, engine="openpyxl")
        if name.endswith(".csv"):
            return _read_csv(data)
    except ImportFileError:
        raise
    except Exception as exc:
        raise ImportFileError("Faylni o'qib bo'lmadi. Fayl buzilgan yoki formati noto'g'ri.") from exc
    raise ImportFileError("Fayl turi qo'llab-quvvatlanmaydi (.xlsx yoki .csv).")


def run_import(job: ImportJob) -> None:
    df = read_table(job)
    mapping = map_columns(df.columns)
    missing = [f for f in REQUIRED if f not in mapping.values()]
    if missing:
        raise ImportFileError(
            f"Kerakli ustunlar topilmadi: {', '.join(missing)}. Birinchi qatorda code, name, price bo'lishi kerak."
        )
    df = df[list(mapping)].rename(columns=mapping)

    # Butunlay bo'sh qatorlarni tashlaymiz (asl qator raqami indeksda saqlanadi)
    blank = df.apply(lambda col: col.astype(str).str.strip() == "").all(axis=1)
    df = df[~blank]
    if len(df) > MAX_ROWS:
        raise ImportFileError(f"Fayl juda katta: {MAX_ROWS} qatordan oshmasligi kerak.")

    errors, valid = [], {}
    for idx, raw in zip(df.index, df.to_dict("records")):
        row = int(idx) + 2  # sarlavha + 0-dan boshlanadi
        clean, reason = validate_row(raw)
        if clean is None:
            errors.append({"row": row, "reason": reason, "code": clean_text(raw.get("code")),
                           "name": clean_text(raw.get("name")), "price": clean_text(raw.get("price"))})
            continue
        previous = valid.get(clean["code"])
        if previous:  # takroriy kod: oxirgisi qoladi, oldingisi xato sifatida qaytadi
            errors.append({"row": previous[0], "reason": "Takroriy kod (keyingi qator olindi)",
                           "code": clean["code"], "name": previous[1]["name"], "price": str(previous[1]["price"])})
        valid[clean["code"]] = (row, clean)

    codes = list(valid)
    existing = {}
    for i in range(0, len(codes), LOOKUP_CHUNK):
        chunk = codes[i:i + LOOKUP_CHUNK]
        for product in Product.objects.filter(shop_id=job.shop_id, code__in=chunk):
            existing[product.code] = product

    now = timezone.now()
    to_create, to_update = [], []
    for code, (_, c) in valid.items():
        product = existing.get(code)
        if product is None:
            to_create.append(Product(shop_id=job.shop_id, code=code, name=c["name"], price=c["price"],
                                     cost_price=c["cost_price"] or 0, unit=c["unit"] or "dona"))
        else:
            product.name, product.price, product.is_active = c["name"], c["price"], True
            if c["cost_price"] is not None:
                product.cost_price = c["cost_price"]
            if c["unit"]:
                product.unit = c["unit"]
            product.updated_at = now
            to_update.append(product)

    with transaction.atomic():
        Product.objects.bulk_create(to_create, batch_size=1000)
        Product.objects.bulk_update(
            to_update, ["name", "price", "cost_price", "unit", "is_active", "updated_at"], batch_size=1000)

    errors.sort(key=lambda e: e["row"])
    job.total = len(df)
    job.created = len(to_create)
    job.updated = len(to_update)
    job.skipped = len(errors)
    job.errors = errors[:MAX_ERRORS_STORED]
    job.status = ImportJob.Status.DONE
    job.save()
    