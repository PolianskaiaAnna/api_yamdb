from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework import filters, viewsets, permissions

from api.filters import FilterForTitle
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleReadSerializer,
                             TitleWriteSerializer,
                             ReviewSerializer,
                             CommentSerializer,)
from api.mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre, Title, Review
from users.permissions import IsOwnerOrReadOnly
from .permissions import IsAuthorOrModeratorOrAdmin


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    # queryset = Title.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, )
    filterset_class = FilterForTitle
    ordering_fields = ('name',)

    def get_queryset(self):
        queryset = Title.objects.annotate(rating=Avg('reviews__score'))
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin,
    )
    http_method_names = ["get", "post", "patch", "delete"]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin,
    )
    http_method_names = ["get", "post", "patch", "delete"]

    def get_review(self):
        get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
