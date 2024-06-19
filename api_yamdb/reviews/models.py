from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

User = get_user_model()





class Category(models.Model):
    """Модель категории(типа) произведения."""

    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
        validators=[validate_slug],
    )
    name = models.CharField(
        'Название',
        max_length=200,
    )

    def __str__(self):
        return self.name
