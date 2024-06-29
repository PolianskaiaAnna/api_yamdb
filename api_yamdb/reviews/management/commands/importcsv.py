
import csv

from django.core.management.base import BaseCommand

from api_yamdb.settings import Path
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Импорт данных csv из /static/data/ в базу данных.'

    def handle(self, *args, **kwargs):
        CSV_DIR = Path('static', 'data')
        FILE_HANDLE = (
            ('category.csv', Category, {}),
            ('genre.csv', Genre, {}),
            ('users.csv', User, {}),
            ('titles.csv', Title, {'category': 'category_id'}),
            ('genre_title.csv', Title.genre.through, {}),
            ('review.csv', Review, {'author': 'author_id'}),
            ('comments.csv', Comment, {'author': 'author_id'}),
        )
        for file, model, replace in FILE_HANDLE:
            self.stdout.write(f'Начинаем импорт из файла {file}')
            with open(Path(CSV_DIR, file), mode='r', encoding='utf8') as f:
                reader = csv.DictReader(f)
                counter = 0
                objects_to_create = []
                for row in reader:
                    counter += 1
                    args = dict(**row)
                    if replace:
                        for old, new in replace.items():
                            args[new] = args.pop(old)
                    objects_to_create.append(model(**args))
                model.objects.bulk_create(objects_to_create,
                                          ignore_conflicts=True)
                self.stdout.write(
                    f'Данные из файла {file} импортированы')

        self.stdout.write(self.style.SUCCESS(
            'Все данные загружены из csv файлов загружены в базу')
        )
