from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, SignUpView, TokenView, UserProfileAPIView

router_vers1 = DefaultRouter()
router_vers1.register('v1/users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', UserProfileAPIView.as_view(), name='profile'),
    path('', include(router_vers1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='check_token'),
]
