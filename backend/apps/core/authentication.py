from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings


class JWTAuth(JWTAuthentication):
    """Foydalanuvchini shop bilan BITTA so'rovda oladi (N+1 yo'q)."""

    def get_user(self, validated_token):
        User = get_user_model()
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            user = User.objects.select_related("shop").get(**{api_settings.USER_ID_FIELD: user_id})
        except (KeyError, User.DoesNotExist):
            raise AuthenticationFailed("Foydalanuvchi topilmadi.", code="user_not_found")
        if not user.is_active:
            raise AuthenticationFailed("Hisob o'chirilgan.", code="user_inactive")
        return user
