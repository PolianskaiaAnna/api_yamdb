from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer

User = get_user_model()


class SignUpView(APIView):
    """Класс, рписывающий запросы на получение кода регистрации"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(generics.CreateAPIView):
    """Класс, описывающий создание токена"""
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(token, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Класс, описывающий запросы к модели User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
