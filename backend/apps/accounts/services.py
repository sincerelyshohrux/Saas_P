import secrets

from django.core.cache import cache

MAX_FAILS = 5
LOCK_SECONDS = 15 * 60


def generate_temp_password() -> str:
    return secrets.token_urlsafe(9)


def lockout_key(username: str) -> str:
    return f"login_fail:{username.lower()}"


def reset_password(user) -> str:
    """Vaqtinchalik parol beradi, majburiy almashtirishni yoqadi, blokni ochadi."""
    password = generate_temp_password()
    user.set_password(password)
    user.must_change_password = True
    user.save(update_fields=["password", "must_change_password"])
    cache.delete(lockout_key(user.username))
    return password
