import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import AccessToken

LENG_EMAIL = 254
LENG_USER = 150

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Класс, описывающий сериализатор, для проверки нового пользователя"""
    email = serializers.EmailField(
        max_length=LENG_EMAIL, required=True
    )
    username = serializers.CharField(
        max_length=LENG_USER, required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """
        Функция проверяет, что юзернейм соответствует заданному составу,
        а также, что связка юзернейм-email уникальна"""
        email = data.get('email')
        username = data.get('username')
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                'Юзернейм содержит недопустимые символы.'
            )
        if username == 'me':
            raise serializers.ValidationError('Нельзя использовать имя me')
        try:
            # Проверка на то, что нельзя использовать email,
            # уже зарегистрированного пользователя
            user_with_email = User.objects.get(email=email)
            if user_with_email.username != username:
                raise serializers.ValidationError(
                    'Пользователь с таким email уже зарегистрирован'
                )
        except User.DoesNotExist:
            pass

        try:
            # Проверка на то, что нельзя использовать занятый юзернейм
            user_with_username = User.objects.get(username=username)
            if user_with_username.email != email:
                raise serializers.ValidationError(
                    'Пользователь с таким именем уже зарегистрирован'
                )
        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        """
        Функция создает нового пользователя или
        получает уже зарегистрированного из базы
        """
        email = validated_data['email']
        username = validated_data['username']
        user, created = User.objects.get_or_create(
            username=username, defaults={'email': email}
        )
        self.send_activation_email(user)

        return user

    def send_activation_email(self, user):
        """Функция отправляет код активации на имейл"""
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код активации для проекта YAMDB',
            message=(
                f'Ваш код для получения токена.\n'
                f'confirmation code: {confirmation_code}\n'
                f'username: {user.username}'
            ),
            from_email='admin@yamdb.yamdb',
            recipient_list=[user.email],
            fail_silently=False,
        )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для выдачи токена"""
    username = serializers.CharField(max_length=LENG_USER)
    confirmation_code = serializers.CharField(max_length=LENG_USER)

    def validate(self, data):
        """ Функция проверяет валидность связки юзернейм+код"""
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('Пользователь не найден')

        check_token = default_token_generator.check_token(
            user,
            confirmation_code
        )
        if not check_token:
            raise serializers.ValidationError('Неверный код активации')
        return data

    def create(seld, validated_data):
        """Функция создает токен и возвращает его"""
        user = User.objects.get(username=validated_data['username'])
        token = AccessToken.for_user(user)
        return {'token': str(token)}


class UserSerializer(serializers.ModelSerializer):
    """Класс, описывающий сериализатор для модели User"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, data):
        """
        Проверка, что юзернейм соответствует заданному составу
        """
        if not re.match(r'^[\w.@+-]+\Z', data):
            raise serializers.ValidationError(
                'Юзернейм содержит недопустимые символы.'
            )
        return data
