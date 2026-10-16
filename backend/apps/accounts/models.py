from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "SUPER_ADMIN")
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super admin"
        SHOP_ADMIN = "SHOP_ADMIN", "Dokon admin"
        AGENT = "AGENT", "Agent"
        CUSTOMER = "CUSTOMER", "Mijoz"

    objects = UserManager()

    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    shop = models.ForeignKey("shops.Shop", null=True, blank=True,
                             on_delete=models.CASCADE, related_name="users")
    must_change_password = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        indexes = [models.Index(fields=["shop", "role"])]
        constraints = [
            # SUPER_ADMIN dokonsiz, qolgan rollar albatta dokon bilan
            models.CheckConstraint(
                condition=models.Q(role="SUPER_ADMIN", shop__isnull=True)
                | (~models.Q(role="SUPER_ADMIN") & models.Q(shop__isnull=False)),
                name="user_role_shop_consistent",
            ),
        ]
