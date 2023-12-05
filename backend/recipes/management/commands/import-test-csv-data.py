import csv
import os
from typing import Type

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Model

from ...models import Ingredient, Recipe

User = get_user_model()

DATA_DIRECTORY = "data"

MODEL_MAPPING = {
    "ingredients.csv": Ingredient,
}


class Command(BaseCommand):
    help = (
        "Import sample data from a set of pre-uploaded CSV files "
        "into corresponding database tables to generate "
        "test instances of recipes app models"
    )

    def replace_field_name(self, fields, find, replace):
        fields[replace] = fields.pop(find)

    def set_instance_from_id(self, fields, foreign_key, model: Type[Model]):
        primary_key = fields.pop(foreign_key)
        fields[foreign_key] = model.objects.get_or_create(
            id=int(primary_key)
        )[0]

    def handle_fields(self, fields, model: Type[Model]):
        if model == Recipe:
            self.replace_field_name(fields, "title", "name")
            self.set_instance_from_id(fields, "author", User)

    def parse_table(self, table_path, model: Type[Model]):
        with open(file=table_path, mode="r", encoding="utf-8") as table:
            data = []
            reader = csv.DictReader(table)
            for row in reader:
                self.handle_fields(row, model)
                data.append(model(**row))
            model.objects.all().delete()
            model.objects.bulk_create(data)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for table_name, model in MODEL_MAPPING.items():
            table_path = os.path.join(DATA_DIRECTORY, table_name)
            self.parse_table(table_path, model)
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
