from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, SignUpView, TokenView

router_v1 = DefaultRouter()
router_v1.register(r'v1/users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', SignUpView.as_view()),
]