import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.shops.models import Shop

PASSWORD = "pass12345"


@pytest.fixture(autouse=True)
def _clear_cache():
    cache.clear()


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def super_admin(db):
    return User.objects.create_user("root", password=PASSWORD, role=User.Role.SUPER_ADMIN)


@pytest.fixture
def shop(db):
    return Shop.objects.create(name="Dokon A", slug="dokon-a")


@pytest.fixture
def shop_admin(shop):
    return User.objects.create_user("a_admin", password=PASSWORD, role=User.Role.SHOP_ADMIN, shop=shop)
