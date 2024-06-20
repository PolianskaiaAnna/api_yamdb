from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
import re

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    """Класс, описывающий сериализатор, для проверки нового пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email')

    # def validate(self, data):
    #     email = data.get('email')
    #     username = data.get('username')

    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError('Email уже используется')
    #     if User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError('Юзернейм занят')
    #     if username == 'me':
    #         raise serializers.ValidationError('Нельзя использовать имя me')

    #     return data

    def validate_username(self, data):        
        if not re.match(r'^[\w.@+-]+\Z', data):
            raise serializers.ValidationError(
                'Юзернейм содержит недопустимые символы.'
            )
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError('Юзернейм занят')
        if data == 'me':
            raise serializers.ValidationError('Нельзя использовать имя me')
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError('Email уже используется')
        return data        

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        user = User.objects.create(username=username, email=email)
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
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для выдачи токена"""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = User.objects.get(username=username)

        check_token = default_token_generator.check_token(
            user,
            confirmation_code
        )
        if not check_token:
            raise serializers.ValidationError('Неверный код активации')
        return data

    def create(seld, validated_data):
        user = User.objects.get(username=validated_data['username'])
        token = AccessToken.for_user(user)
        return {'token': str(token)}


class UserSerializer(serializers.ModelSerializer):
    """Класс, описывающий сериализатор для модели User"""
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
