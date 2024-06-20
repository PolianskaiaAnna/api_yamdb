from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from reviews.models import User
from api.serializers import SignupSerializer

class SignUpView(APIView):
    """Класс, описывающий регистрацию пользователя и отправку кода подтверждения"""
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('username')
            email = request.data.get('email')
            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)

            send_mail(
                subject='Код активации для проекта YAMDB',
                message=(
                    f'Ваш код для получения токена.\n'
                    f'confirmation code: {confirmation_code}\n'
                    f'username: {username}'
                ),
                from_email='admin@yamdb.yamdb',
                recipient_list=[email],
                fail_silently=False,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        

# class TokenView(ApiView)

# token = AccessToken.for_user(user)
#     return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer