from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class CustomUser(AbstractUser):
    """Класс, описывающий кастомную модель пользователя"""
    username = models.CharField(
        'Имя пользователя', max_length=150,
        unique=True
    )
    email = models.EmailField('Email', max_length=254, unique=True)
    first_name = models.CharField('Имя', blank=True, max_length=150)
    last_name = models.CharField('Фамилия', blank=True, max_length=150)
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        'Роль', choices=USER_ROLES, default=USER_ROLES[0][1], max_length=150
    )


User = get_user_model()
