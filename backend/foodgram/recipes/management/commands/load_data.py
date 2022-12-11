import csv
import datetime

from django.core.management import BaseCommand

from recipes.models import Ingredients, Tag

csv_files = (
    (Tag, 'tags.csv'),
    (Ingredients, 'ingredients.csv')
)

fields = (
    ('name', 'colour', 'slug'),
    ('name', 'measurement')
)


class Command(BaseCommand):
    help = ("Загрузка data из data/*.csv."
            "Запуск: python manage.py load_csv_data."
            "Подробнее об импорте в README.md.")

    @staticmethod
    def clear_tables():
        Tag.objects.all().delete()
        Ingredients.objects.all().delete()
 
    def handle(self, *args, **options):
        self.clear_tables()
        print("Старт импорта")
        start_time = datetime.datetime.now()

        try:
            for model, file in csv_files:
                with open(
                        f'recipes/data/{file}', encoding='utf-8'
                ) as f:
                    reader = csv.DictReader(f, delimiter=',')
                    for row in reader:
                        if model in fields:
                            row[fields[model][2]] = row.pop(fields[model][0])
                        obj, created = model.objects.get_or_create(**row)
                        if created:
                            print(f'{obj} загружен в таблицу {model.__name__}')
                        print(
                            f'{obj} уже загружен в таблицу {model.__name__}')

            print(f"Загрузка данных завершена за"
                  f" {(datetime.datetime.now() - start_time).total_seconds()} "
                  f"сек.")

        except Exception as error:
            print(f"Сбой в работе импорта: {error}.")

        finally:
            print("Завершена работа импорта.")