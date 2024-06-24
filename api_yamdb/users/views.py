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


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API view для просмотра и обновления профиля пользователя.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        """
        Обновление профиля пользователя.
        """
        user = self.get_object()
        if 'role' in request.data:
            return Response({'error': 'Нельзя менять роль'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """
        Получение профиля пользователя.
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Класс, описывающий запросы к модели User"""
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    pagination_class = PageNumberPagination
    permission_classes = [IsAdmin]

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

    def update(self, request, *args, **kwargs):
        """Функция обрабатывает PUT-запросы для обновления профиля"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        """
        Функция обрабатывает GET-запросы для получения
        списка всех пользователей с учетом пагинации
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})
