from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий (типов) произведений."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
