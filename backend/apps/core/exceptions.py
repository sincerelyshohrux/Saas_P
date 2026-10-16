from rest_framework.exceptions import APIException, ValidationError


class PasswordChangeRequired(APIException):
    status_code = 403
    default_detail = "Avval parolni almashtiring."
    default_code = "password_change_required"


class SubscriptionExpired(APIException):
    status_code = 403
    default_detail = "Obuna muddati tugagan."
    default_code = "subscription_expired"


class ShopBlocked(APIException):
    status_code = 403
    default_detail = "Dokon bloklangan."
    default_code = "shop_blocked"


class InvalidCredentials(APIException):
    status_code = 400
    default_detail = "Login yoki parol noto'g'ri."
    default_code = "invalid_credentials"


class AccountLocked(APIException):
    status_code = 423
    default_detail = "Juda ko'p xato urinish. Keyinroq qayta urinib ko'ring."
    default_code = "account_locked"


def api_exception_handler(exc, context):
    """Barcha xatolarni {code, detail, fields?} shakliga keltiradi."""
    # Import shu yerda: DRF sozlamalari yuklanayotganda aylanma importni oldini oladi
    from rest_framework.views import exception_handler

    response = exception_handler(exc, context)
    if response is None:
        return None

    data = response.data
    if isinstance(exc, ValidationError):
        fields = data if isinstance(data, dict) else {"non_field_errors": data}
        response.data = {"code": "validation_error", "detail": "Ma'lumotlar noto'g'ri.", "fields": fields}
        return response

    if isinstance(data, dict):
        detail = data.get("detail", "")
        code = data.get("code") or getattr(detail, "code", None)
    else:
        detail, code = data, None
    code = code or getattr(exc, "default_code", None) or "error"
    response.data = {"code": str(code), "detail": str(detail)}
    return response
