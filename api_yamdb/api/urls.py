from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
#from users.views import UsersViewSet, SignUpView, TokenView, UserProfileAPIView

router_vers1 = routers.DefaultRouter()

#router_vers1.register(r'v1/users', UsersViewSet, basename='users')
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
#    path('v1/users/me/', UserProfileAPIView.as_view(), name='profile'),
#    path('', include(router_vers1.urls)),
#    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
#   path('v1/auth/token/', TokenView.as_view(), name='check_token'),
]
