from rest_framework.routers import DefaultRouter
from .views import ShopViewSet

router = DefaultRouter()
router.register("admin/shops", ShopViewSet, basename="admin-shop")
urlpatterns = router.urls
