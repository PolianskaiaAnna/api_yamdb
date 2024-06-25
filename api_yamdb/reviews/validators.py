from datetime import datetime

from django.core.exceptions import ValidationError


def validation_year(value):
    """Проверка года"""

    if value >= datetime.now().year:
        raise ValidationError(
            message=f'Год {value}, превышает текущий!',
            params={'value': value},
        )


def validation_score(value):
    """Проверка оценки"""
    if not 1 <= value <= 10:
        raise ValidationError('Оценка должна быть от 1 до 10.')
