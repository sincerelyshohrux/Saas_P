from rest_framework import serializers

from apps.accounts.models import User
from .models import Shop

SHOP_FIELDS = ["name", "slug", "phone", "region", "address", "latitude", "longitude"]


class ShopSerializer(serializers.ModelSerializer):
    admin_username = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ["id", *SHOP_FIELDS, "is_active", "plan_expires_at", "created_at", "admin_username"]
        read_only_fields = ["id", "slug", "created_at"]

    def get_admin_username(self, obj):
        admins = getattr(obj, "admins", None)  # ViewSet prefetch qiladi
        if admins is None:
            admins = list(obj.users.filter(role=User.Role.SHOP_ADMIN)[:1])
        return admins[0].username if admins else None


class ShopCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, max_length=150)

    class Meta:
        model = Shop
        fields = [*SHOP_FIELDS, "username"]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Bu login band.")
        return value


class SubscriptionSerializer(serializers.Serializer):
    plan_expires_at = serializers.DateTimeField(allow_null=True)
