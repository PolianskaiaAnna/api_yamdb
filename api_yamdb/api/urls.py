from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router_vers1 = routers.DefaultRouter()

router_vers1.register(
    r'categories', CategoryViewSet, basename='categories'
)
router_vers1.register(
    r'genres', GenreViewSet, basename='genres'
)
router_vers1.register(
    r'titles', TitleViewSet, basename='titles'
)

urlpatterns = [
    path('v1/', include(router_vers1.urls)),
]
