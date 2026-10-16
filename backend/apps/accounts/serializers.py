from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    shop_id = serializers.UUIDField(read_only=True, allow_null=True)
    shop_name = serializers.CharField(source="shop.name", read_only=True, default=None)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "role", "shop_id", "shop_name", "must_change_password"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(trim_whitespace=False)
    new_password = serializers.CharField(trim_whitespace=False)

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Joriy parol noto'g'ri.")
        return value

    def validate(self, attrs):
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError({"new_password": ["Yangi parol eskisidan farq qilishi kerak."]})
        validate_password(attrs["new_password"], user=self.context["request"].user)
        return attrs
