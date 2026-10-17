from pathlib import Path

from django.conf import settings
from django.db import models

from apps.core.models import TenantModel


class Product(TenantModel):
    code = models.CharField(max_length=50)  # mahsulot raqami (dokon ichida noyob)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    cost_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)  # tannarx (foyda uchun)
    unit = models.CharField(max_length=20, default="dona")
    # Ombor qoldig'i: StockMovement (ledger) dan hisoblangan KESH. Faqat inventory.services o'zgartiradi.
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(fields=["shop", "code"], name="uniq_shop_product_code"),
            models.CheckConstraint(condition=models.Q(stock__gte=0), name="product_stock_non_negative"),
            models.CheckConstraint(
                condition=models.Q(price__gte=0) & models.Q(cost_price__gte=0),
                name="product_prices_non_negative",
            ),
        ]
        indexes = [
            models.Index(fields=["shop", "name"]),
            models.Index(fields=["shop", "is_active"]),
        ]

    def __str__(self):
        return f"{self.code} {self.name}"


def import_upload_path(instance, filename):
    return f"imports/{instance.shop_id}/{instance.id}{Path(filename).suffix.lower()}"


class ImportJob(TenantModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        PROCESSING = "processing"
        DONE = "done"
        FAILED = "failed"

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=import_upload_path)
    total = models.PositiveIntegerField(default=0)
    created = models.PositiveIntegerField(default=0)
    updated = models.PositiveIntegerField(default=0)
    skipped = models.PositiveIntegerField(default=0)
    errors = models.JSONField(default=list, blank=True)  # [{row, reason, code, name, price}]
    error_message = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="+")

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["shop", "-created_at"])]