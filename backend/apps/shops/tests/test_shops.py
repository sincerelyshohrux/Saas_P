from datetime import timedelta

import pytest
from django.utils import timezone

from apps.accounts.models import User

pytestmark = pytest.mark.django_db

URL = "/api/v1/admin/shops/"
ME = "/api/v1/auth/me/"


def fresh(user):
    """Keshlangan shop obyektisiz yangi nusxa (DB dagi hozirgi holat)."""
    return User.objects.select_related("shop").get(pk=user.pk)


def test_super_admin_creates_shop_with_temp_password(api, super_admin):
    api.force_authenticate(super_admin)
    r = api.post(URL, {"name": "Bolalar dunyosi", "slug": "bolalar", "username": "bolalar_admin",
                       "region": "tashkent_city"}, format="json")
    assert r.status_code == 201
    assert r.data["temp_password"]
    assert r.data["admin_username"] == "bolalar_admin"
    user = User.objects.get(username="bolalar_admin")
    assert user.must_change_password and user.role == "SHOP_ADMIN"
    assert user.check_password(r.data["temp_password"])
    assert "temp_password" not in api.get(f"{URL}{r.data['id']}/").data  # faqat bir marta


def test_duplicate_slug_and_username(api, super_admin, shop, shop_admin):
    api.force_authenticate(super_admin)
    r = api.post(URL, {"name": "X", "slug": shop.slug, "username": "yangi"}, format="json")
    assert r.status_code == 400 and "slug" in r.data["fields"]
    r = api.post(URL, {"name": "X", "slug": "x", "username": "A_ADMIN"}, format="json")
    assert r.status_code == 400 and "username" in r.data["fields"]


def test_shop_admin_cannot_access_admin_api(api, shop_admin):
    api.force_authenticate(shop_admin)
    assert api.get(URL).status_code == 403
    assert api.post(URL, {}, format="json").status_code == 403


def test_toggle_active_blocks_shop_users(api, super_admin, shop, shop_admin):
    api.force_authenticate(super_admin)
    r = api.post(f"{URL}{shop.id}/toggle-active/")
    assert r.status_code == 200 and r.data["is_active"] is False

    api.force_authenticate(fresh(shop_admin))
    r = api.get(ME)
    assert r.status_code == 403 and r.data["code"] == "shop_blocked"


def test_expired_subscription_blocks(api, shop, shop_admin):
    shop.plan_expires_at = timezone.now() - timedelta(days=1)
    shop.save()
    api.force_authenticate(fresh(shop_admin))
    r = api.get(ME)
    assert r.status_code == 403 and r.data["code"] == "subscription_expired"


def test_reset_password_forces_change(api, super_admin, shop, shop_admin):
    api.force_authenticate(super_admin)
    r = api.post(f"{URL}{shop.id}/reset-password/")
    assert r.status_code == 200
    shop_admin.refresh_from_db()
    assert shop_admin.must_change_password
    assert shop_admin.check_password(r.data["temp_password"])


def test_update_cannot_change_slug(api, super_admin, shop):
    api.force_authenticate(super_admin)
    r = api.patch(f"{URL}{shop.id}/", {"slug": "hack", "name": "Yangi nom"}, format="json")
    assert r.status_code == 200
    shop.refresh_from_db()
    assert shop.slug == "dokon-a" and shop.name == "Yangi nom"


def test_map_returns_only_shops_with_coordinates(api, super_admin, shop):
    api.force_authenticate(super_admin)
    assert api.get(f"{URL}map/").data == []
    shop.latitude, shop.longitude = "41.311081", "69.240562"
    shop.save()
    assert len(api.get(f"{URL}map/").data) == 1
