import csv

from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_tags()
        print('Загрузка тэгов завершена.')

    def import_tags(self, file='tags.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./data/{file}'
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                Tag.objects.update_or_create(
                    name=row[0], color=row[1], slug=row[2]
                )
