from rest_framework import serializers

from reviews.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Класс, описывающий сериализатор, для проверки нового пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    """Класс, описывающий сериализатор для модели User"""
    class Meta:
        model = User
        fields = '__all__'

