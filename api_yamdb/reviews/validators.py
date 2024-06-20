from datetime import datetime

from django.core.exceptions import ValidationError


def validation_year(value):
    """Проверка года"""

    if value >= datetime.now().year:
        raise ValidationError(
            message=f'Год {value}, превышает текущий!',
            params={'value': value},
        )
