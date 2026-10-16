from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class Region(models.TextChoices):
    TASHKENT_CITY = "tashkent_city", "Toshkent shahri"
    TASHKENT = "tashkent", "Toshkent viloyati"
    ANDIJAN = "andijan", "Andijon"
    BUKHARA = "bukhara", "Buxoro"
    FERGANA = "fergana", "Farg'ona"
    JIZZAKH = "jizzakh", "Jizzax"
    KASHKADARYA = "kashkadarya", "Qashqadaryo"
    KHOREZM = "khorezm", "Xorazm"
    NAMANGAN = "namangan", "Namangan"
    NAVOI = "navoi", "Navoiy"
    SAMARKAND = "samarkand", "Samarqand"
    SURKHANDARYA = "surkhandarya", "Surxondaryo"
    SYRDARYA = "syrdarya", "Sirdaryo"
    KARAKALPAKSTAN = "karakalpakstan", "Qoraqalpog'iston"


class Shop(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # Telegram havola uchun, o'zgarmaydi
    phone = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=30, choices=Region.choices, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
    is_active = models.BooleanField(default=True)
    plan_expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_active", "region"])]

    def __str__(self):
        return self.name
