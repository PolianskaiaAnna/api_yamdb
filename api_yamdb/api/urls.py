from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet
)

router_vers1 = routers.DefaultRouter()

router_vers1.register(
    'categories', CategoryViewSet, basename='categories'
)
router_vers1.register(
    'genres', GenreViewSet, basename='genres'
)
router_vers1.register(
    'titles', TitleViewSet, basename='titles'
)
router_vers1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_vers1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_vers1.urls)),
]
