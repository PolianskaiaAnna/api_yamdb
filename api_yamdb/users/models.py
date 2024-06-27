from django.db import models
from django.contrib.auth.models import AbstractUser


LENG_EMAIL = 254
LENG_USER = 150


class User(AbstractUser):
    """Класс, описывающий кастомную модель пользователя"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=LENG_USER,
        unique=True
    )
    email = models.EmailField(
        'Email', max_length=LENG_EMAIL, unique=True
    )
    first_name = models.CharField(
        'Имя', blank=True, max_length=LENG_USER
    )
    last_name = models.CharField(
        'Фамилия', blank=True, max_length=LENG_USER
    )
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(
        'Роль', choices=USER_ROLES,
        default=USER, max_length=LENG_USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Ползователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
