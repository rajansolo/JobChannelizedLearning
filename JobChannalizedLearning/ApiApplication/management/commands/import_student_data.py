# import_internship_data.py
import json
from django.core.management.base import BaseCommand
from ApiApplication.models import Field

class Command(BaseCommand):
    help = 'Imports Field data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path) as json_file:
            data = json.load(json_file)

            for item in data:
                Field_data = Field(
                    Name=item['Name'],
                    Company=item['Company'],
                    Role=item['Role'],
                    Date=item['Date'],
                    InternshipDuration=item['InternshipDuration'],
                    Intake=item['Intake'],
                )
                Field_data.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
