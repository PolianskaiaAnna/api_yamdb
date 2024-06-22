from django.contrib.auth import get_user_model
from rest_framework import filters, generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdmin, IsAuthenticated
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer

User = get_user_model()


class SignUpView(APIView):
    """Класс, описывающий запросы на получение кода регистрации"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Функция обрабатывает POST-запрос при регистрации пользователя"""
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(generics.CreateAPIView):
    """Класс, описывающий создание токена"""
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Функция обрабатывает POST запрос для создания токена"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(token, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Класс, описывающий запросы к модели User"""
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    pagination_class = PageNumberPagination

    def get_permissions(self):
        """Функция определяет разрешения доступа для разных типов запросов"""
        if self.action in [
            'list', 'create', 'retrieve', 'partial_update', 'update', 'destroy'
        ]:
            permission_classes = [IsAdmin]
        elif self.action == 'profile':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'profile':
            return User.objects.filter(username=self.request.user.username)
        return super().get_queryset()

    def profile(self, request):
        """
        Функция позволяет пользователю просматривать и обновлять свой профиль
        """
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(email=user.email, role=user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Функция обрабатывает PUT-запросы для обновления профиля"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        Функция обрабатываает DELETE-запросы на удаление профиля пользователя
        """
        user = get_object_or_404(User, username=request.user.username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        """
        Функция обрабатываает PATCH-запросы на частичное
        изменение профиля пользователя
        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Функция обрабатывает GET-запросы для получения
        списка всех пользователей
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})
