from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.exceptions import AccountLocked, InvalidCredentials
from .serializers import ChangePasswordSerializer, LoginSerializer, UserSerializer
from .services import LOCK_SECONDS, MAX_FAILS, lockout_key


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        key = lockout_key(username)

        if cache.get(key, 0) >= MAX_FAILS:
            raise AccountLocked()

        user = authenticate(request=request, username=username, password=serializer.validated_data["password"])
        if user is None:
            cache.add(key, 0, LOCK_SECONDS)
            cache.incr(key)
            raise InvalidCredentials()

        cache.delete(key)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            RefreshToken(request.data.get("refresh", "")).blacklist()
        except TokenError:
            pass  # allaqachon yaroqsiz, baribir 204
        return Response(status=204)


class MeView(APIView):
    allow_pending_password = True

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    allow_pending_password = True

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])
        return Response(status=204)
