import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

FILE_TO_OPEN = "./data/ingredients.csv"


class Command(BaseCommand):
    help = "Импорт ингредиентов в базу данных"

    def handle(self, **kwargs):
        with open(
            FILE_TO_OPEN, "r", encoding="UTF-8"
        ) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
