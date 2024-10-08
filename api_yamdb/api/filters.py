from django_filters import rest_framework as filters
from reviews.models import Title


class FilterForTitle(filters.FilterSet):
    """
    Фильтр названий, категорй и жанров произведений по слагу.
    """
    name = filters.CharFilter(field_name='name',
                              lookup_expr='contains')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
