import pytest

pytestmark = pytest.mark.django_db

LOGIN = "/api/v1/auth/login/"
ME = "/api/v1/auth/me/"
CHANGE = "/api/v1/auth/change-password/"
SHOPS = "/api/v1/admin/shops/"


def test_login_ok(api, super_admin):
    r = api.post(LOGIN, {"username": "root", "password": "pass12345"}, format="json")
    assert r.status_code == 200
    assert {"access", "refresh", "user"} <= r.data.keys()
    assert r.data["user"]["role"] == "SUPER_ADMIN"
    assert r.data["user"]["shop_id"] is None


def test_login_wrong_password(api, super_admin):
    r = api.post(LOGIN, {"username": "root", "password": "xato"}, format="json")
    assert r.status_code == 400
    assert r.data["code"] == "invalid_credentials"


def test_lockout_after_five_failures(api, super_admin):
    for _ in range(5):
        assert api.post(LOGIN, {"username": "root", "password": "xato"}, format="json").status_code == 400
    r = api.post(LOGIN, {"username": "root", "password": "pass12345"}, format="json")
    assert r.status_code == 423


def test_me_requires_auth(api):
    assert api.get(ME).status_code == 401


def test_jwt_flow_with_real_token(api, super_admin):
    r = api.post(LOGIN, {"username": "root", "password": "pass12345"}, format="json")
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {r.data['access']}")
    assert api.get(ME).data["username"] == "root"


def test_forced_password_change_blocks_then_unblocks(api, super_admin):
    super_admin.must_change_password = True
    super_admin.save()
    api.force_authenticate(super_admin)

    r = api.get(SHOPS)
    assert r.status_code == 403 and r.data["code"] == "password_change_required"
    assert api.get(ME).status_code == 200  # ruxsat berilgan

    r = api.post(CHANGE, {"old_password": "pass12345", "new_password": "N3w-Strong-Pass!"}, format="json")
    assert r.status_code == 204
    assert api.get(SHOPS).status_code == 200


def test_change_password_wrong_old(api, super_admin):
    api.force_authenticate(super_admin)
    r = api.post(CHANGE, {"old_password": "x", "new_password": "N3w-Strong-Pass!"}, format="json")
    assert r.status_code == 400
    assert "old_password" in r.data["fields"]
