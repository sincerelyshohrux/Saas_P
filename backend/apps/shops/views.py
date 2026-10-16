from django.db.models import Prefetch
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.accounts.models import User
from apps.core.permissions import IsSuperAdmin
from .models import Shop
from .serializers import ShopCreateSerializer, ShopSerializer, SubscriptionSerializer
from .services import create_shop_with_admin, reset_shop_admin_password


class ShopViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """DELETE yo'q: dokonni o'chirish hamma ma'lumotni yo'qotadi. Buning o'rniga toggle-active."""
    permission_classes = [IsSuperAdmin]
    serializer_class = ShopSerializer
    filterset_fields = ["is_active", "region"]
    search_fields = ["name", "phone", "slug"]
    ordering_fields = ["created_at", "name", "plan_expires_at"]

    def get_queryset(self):
        admins = User.objects.filter(role=User.Role.SHOP_ADMIN)
        return Shop.objects.prefetch_related(Prefetch("users", queryset=admins, to_attr="admins"))

    def create(self, request, *args, **kwargs):
        serializer = ShopCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        username = data.pop("username")
        shop, password = create_shop_with_admin(username=username, **data)
        return Response({**ShopSerializer(shop).data, "temp_password": password}, status=201)

    @action(detail=True, methods=["post"], url_path="reset-password")
    def reset_password(self, request, pk=None):
        password = reset_shop_admin_password(self.get_object())
        if password is None:
            raise NotFound("Dokon admini topilmadi.")
        return Response({"temp_password": password})

    @action(detail=True, methods=["post"], url_path="toggle-active")
    def toggle_active(self, request, pk=None):
        shop = self.get_object()
        shop.is_active = not shop.is_active
        shop.save(update_fields=["is_active", "updated_at"])
        return Response({"is_active": shop.is_active})

    @action(detail=True, methods=["post"])
    def subscription(self, request, pk=None):
        shop = self.get_object()
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop.plan_expires_at = serializer.validated_data["plan_expires_at"]
        shop.save(update_fields=["plan_expires_at", "updated_at"])
        return Response(ShopSerializer(shop).data)

    @action(detail=False, methods=["get"], pagination_class=None)
    def map(self, request):
        rows = (Shop.objects.filter(latitude__isnull=False, longitude__isnull=False)
                .values("id", "name", "latitude", "longitude", "region"))
        return Response(list(rows))
