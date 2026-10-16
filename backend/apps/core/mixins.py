class TenantViewSetMixin:
    """shop_id FAQAT request.user dan olinadi. Klient yuborgan shop_id ga hech qachon ishonmaymiz."""

    def get_queryset(self):
        return super().get_queryset().filter(shop_id=self.request.user.shop_id)

    def perform_create(self, serializer):
        serializer.save(shop_id=self.request.user.shop_id)
