import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_tags()

    def import_tags(self, file='tags.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./data/{file}'
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for name, color, slug in reader:
                    Tag.objects.get_or_create(
                        name=name, color=color, slug=slug
                    )
            print('Загрузка тэгов завершена.')
        except FileNotFoundError:
            print(f'Файл {file} не найден')
