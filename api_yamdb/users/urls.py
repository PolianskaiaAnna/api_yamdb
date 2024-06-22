from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, SignUpView, TokenView

from . import views

router_v1 = DefaultRouter()
router_v1.register(r'v1/users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', views.UsersViewSet.as_view(
        actions={'get': 'profile', 'patch': 'profile'}
    )),
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='check_token'),
]
