import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_ingredients()

    def import_ingredients(self, file='ingredients.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./data/{file}'
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for name, measurement_unit in reader:
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
            print('Загрузка ингредиентов завершена.')
        except FileNotFoundError:
            print(f'Файл {file} не найден')
