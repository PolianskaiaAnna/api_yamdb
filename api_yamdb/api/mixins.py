from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from users.permissions import IsOwnerOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин Вьюсет для произведений и жанров."""
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['name']
    lookup_field = 'slug'
