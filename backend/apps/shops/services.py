from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.accounts.services import generate_temp_password, reset_password
from .models import Shop


@transaction.atomic
def create_shop_with_admin(*, username, **shop_data):
    shop_data.setdefault("plan_expires_at", timezone.now() + timedelta(days=settings.TRIAL_DAYS))
    shop = Shop.objects.create(**shop_data)
    password = generate_temp_password()
    User.objects.create_user(username=username, password=password, role=User.Role.SHOP_ADMIN,
                             shop=shop, must_change_password=True)
    return shop, password


def reset_shop_admin_password(shop):
    admin = User.objects.filter(shop=shop, role=User.Role.SHOP_ADMIN).order_by("date_joined").first()
    if admin is None:
        return None
    return reset_password(admin)
