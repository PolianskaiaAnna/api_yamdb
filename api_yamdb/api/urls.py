from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet

router_vers1 = routers.DefaultRouter()

router_vers1.register(
    r'categories', CategoryViewSet, basename='categories'
)


urlpatterns = [
    path('v1/', include(router_vers1.urls)),
]
