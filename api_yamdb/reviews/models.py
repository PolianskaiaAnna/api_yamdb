from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

from reviews.validators import validation_year

User = get_user_model()





class CategoryAndGenreModel(models.Model):
    """Абстрактная модель. Добавляет название и слаг."""

    slug = models.SlugField(
        'Slug',
        max_length=settings.LENG_SLUG,
        unique=True,
        validators=[validate_slug],
    )
    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.LENG_CUT]


class Category(CategoryAndGenreModel):
    """Модель категории произведения."""

    class Meta(CategoryAndGenreModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genre(CategoryAndGenreModel):
    """Модель жанра произведений."""

    class Meta(CategoryAndGenreModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Title(models.Model):
    """Модель произведения."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='titles',
    )
    description = models.TextField(
        'Описание',
        db_index=True,
        max_length=settings.LENG_MAX,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    name = models.CharField(
        'Название',
        max_length=settings.LENG_MAX,
        db_index=True,
    )
    year = models.IntegerField(
        'Год выпуска',
        db_index=True,
        validators=(validation_year,),
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
