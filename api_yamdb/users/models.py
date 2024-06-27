from django.db import models
# from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Класс, описывающий кастомную модель пользователя"""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    LENG_EMAIL = 254
    LENG_USER = 150

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
        default=USER_ROLES[0][0], max_length=LENG_USER
    )

    @property
    def is_admin(self):
        return self.role == self.USER_ROLES[2][0] or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLES[1][0]

    @property
    def is_user(self):
        return self.role == self.USER_ROLES[0][0]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}-{self.email}'
