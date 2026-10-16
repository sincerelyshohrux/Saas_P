from django.utils import timezone
from rest_framework.permissions import BasePermission

from .exceptions import PasswordChangeRequired, ShopBlocked, SubscriptionExpired


class IsActiveAccount(BasePermission):
    """
    Har bir so'rovda tekshiradi:
    1) login qilgan, 2) parol almashtirilgan, 3) dokon bloklanmagan, 4) obuna tugamagan.
    View'da `allow_pending_password = True` bo'lsa, 2-tekshiruv o'tkaziladi.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.must_change_password and not getattr(view, "allow_pending_password", False):
            raise PasswordChangeRequired()
        shop = user.shop
        if shop is not None:
            if not shop.is_active:
                raise ShopBlocked()
            if shop.plan_expires_at and shop.plan_expires_at < timezone.now():
                raise SubscriptionExpired()
        return True


class _RolePermission(IsActiveAccount):
    roles: tuple = ()

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in self.roles


class IsSuperAdmin(_RolePermission):
    roles = ("SUPER_ADMIN",)


class IsShopAdmin(_RolePermission):
    roles = ("SHOP_ADMIN",)


class IsShopStaff(_RolePermission):
    roles = ("SHOP_ADMIN", "AGENT")
