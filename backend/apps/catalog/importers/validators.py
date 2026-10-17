"""Import qatorlarini tekshirish: faqat TO'LIQ (kod + nom + narx) qatorlar o'tadi."""
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

REQUIRED = ("code", "name", "price")

# Ustun nomi sinonimlari (kichik harf, apostrof normallashtirilgan)
ALIASES = {
    "code": {"code", "kod", "kodi", "raqam", "raqami", "artikul", "sku", "№",
             "mahsulot raqami", "mahsulot kodi", "код", "артикул"},
    "name": {"name", "nom", "nomi", "mahsulot", "mahsulot nomi", "nomlanishi",
             "наименование", "название"},
    "price": {"price", "narx", "narxi", "sotuv narxi", "цена"},
    "cost_price": {"cost_price", "cost", "tannarx", "tannarxi", "xarid narxi", "себестоимость"},
    "unit": {"unit", "birlik", "o'lchov birligi", "olchov birligi", "ед. изм."},
}
_HEADER_TO_FIELD = {alias: field for field, aliases in ALIASES.items() for alias in aliases}
_APOSTROPHES = str.maketrans({"’": "'", "‘": "'", "ʻ": "'", "ʼ": "'", "`": "'", "\u00a0": " "})
_INT_FLOAT = re.compile(r"^(\d+)\.0+$")  # Excel ba'zan "123.0" beradi
MAX_MONEY = Decimal("999999999999.99")


def normalize_header(value) -> str:
    text = str(value).translate(_APOSTROPHES).strip().lstrip("\ufeff").lower()
    return re.sub(r"\s+", " ", text)


def map_columns(columns) -> dict:
    """Asl ustun nomi -> kanonik maydon. Bir maydonga bir nechta ustun to'g'ri kelsa, birinchisi olinadi."""
    mapping, seen = {}, set()
    for col in columns:
        field = _HEADER_TO_FIELD.get(normalize_header(col))
        if field and field not in seen:
            mapping[col] = field
            seen.add(field)
    return mapping


def clean_text(value) -> str:
    return "" if value is None else str(value).replace("\u00a0", " ").strip()


def parse_money(raw) -> Decimal | None:
    text = clean_text(raw).replace(" ", "").replace(",", ".")
    if not text:
        return None
    try:
        value = Decimal(text)
        if not value.is_finite():
            raise ValueError
        value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError("invalid money")
    if value < 0 or value > MAX_MONEY:
        raise ValueError("out of range")
    return value


def validate_row(raw: dict):
    """Qaytaradi (toza_qator, None) yoki (None, sabab)."""
    code = clean_text(raw.get("code"))
    match = _INT_FLOAT.match(code)
    if match:
        code = match.group(1)
    if not code:
        return None, "Kod yo'q"
    if len(code) > 50:
        return None, "Kod juda uzun (50 belgigacha)"

    name = clean_text(raw.get("name"))
    if not name:
        return None, "Nom yo'q"
    if len(name) > 255:
        return None, "Nom juda uzun (255 belgigacha)"

    if not clean_text(raw.get("price")):
        return None, "Narx yo'q"
    try:
        price = parse_money(raw.get("price"))
    except ValueError:
        return None, "Narx noto'g'ri"
    if price is None or price <= 0:
        return None, "Narx noto'g'ri"

    cost_price = None
    if clean_text(raw.get("cost_price")):
        try:
            cost_price = parse_money(raw.get("cost_price"))
        except ValueError:
            return None, "Tannarx noto'g'ri"

    unit = clean_text(raw.get("unit")) or None
    if unit and len(unit) > 20:
        return None, "Birlik juda uzun (20 belgigacha)"

    return {"code": code, "name": name, "price": price, "cost_price": cost_price, "unit": unit}, None