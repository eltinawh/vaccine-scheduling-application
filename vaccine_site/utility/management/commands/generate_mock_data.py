import csv
import random
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Generate dynamic mock data for any model with fields from CSV and datetime, handling multiple foreign keys'

    def add_arguments(self, parser):
        # Main model arguments
        parser.add_argument('app_label', type=str, help='App name of the main model')
        parser.add_argument('model_name', type=str, help='Model name of the main model')
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

        # Foreign key arguments (accept multiple foreign key mappings)
        parser.add_argument('--fk', nargs='+', type=str, help="Foreign key definitions in the format: 'fk_app,fk_model,fk_field,fk_field_csv'")
        
        # Date and time field arguments
        parser.add_argument('--date-fields', nargs='+', type=str, help="Date field definitions in the format: 'field_name[,end_field_name]'")
        parser.add_argument('--time-fields', nargs='+', type=str, help="Time field definitions in the format: 'field_name[,end_field_name]'")

    def handle(self, *args, **kwargs):
        app_label = kwargs['app_label']
        model_name = kwargs['model_name']
        csv_file = kwargs['csv_file']
        fk_definitions = kwargs['fk']
        date_fields = kwargs['date_fields']
        time_fields = kwargs['time_fields']

        # Get the main model dynamically
        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f'Model {model_name} in app {app_label} not found')

        # Parse the foreign key definitions (list of 'fk_app,fk_model,fk_field,fk_field_csv')
        fk_mappings = []
        for fk_def in fk_definitions:
            try:
                fk_app, fk_model, fk_field, fk_field_csv = fk_def.split(',')
                fk_mappings.append({
                    'fk_app': fk_app,
                    'fk_model': fk_model,
                    'fk_field': fk_field,
                    'fk_field_csv': fk_field_csv,
                })
            except ValueError:
                raise CommandError(f'Invalid foreign key definition: {fk_def}. Use format fk_app,fk_model,fk_field,fk_field_csv')

        # Open the CSV file
        try:
            with open(csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for idx, row in enumerate(reader):
                    
                    row_copy = row.copy()
                    for field in row_copy.keys():
                        # Remove empty field
                        if not row_copy[field]:
                            del row[field]
                    
                        # Handle password
                        if "password" in field:
                            row[field] = make_password(row_copy[field])
                    
                    # Foreign key handling
                    fk_instances = {}
                    for fk in fk_mappings:
                        fk_app = fk['fk_app']
                        fk_model = fk['fk_model']
                        fk_field = fk['fk_field']
                        fk_field_csv = fk['fk_field_csv']

                        try:
                            foreign_model = apps.get_model(fk_app, fk_model)
                        except LookupError:
                            raise CommandError(f'Foreign key model {fk_model} in app {fk_app} not found')

                        fk_value = row.get(fk_field_csv)
                        foreign_instance, created = foreign_model.objects.get_or_create(name=fk_value)  # Adjust the field if not 'name'
                        
                        # Add the foreign key instance to the dictionary to be used in the model creation
                        row[fk_field] = foreign_instance
                        del row[fk_field_csv]

                    # Handle date fields with random days_from_now and end_field_name
                    start_date_range = [1,366]
                    end_date_range = [5,21] # from start date
                    date_values = {}
                    if date_fields:
                        for date_field_def in date_fields:
                            try:
                                parts = date_field_def.split(',')
                                field_name = parts[0]
                                end_field_name = parts[1] if len(parts) > 1 else None

                                # Generate random days from now (e.g., between 0 and 30 days)
                                start_date = timezone.now().date() + timedelta(days=random.randint(*start_date_range))
                                date_values[field_name] = start_date

                                # If there's an end date field, ensure it's later than the start date
                                if end_field_name:
                                    end_date = start_date + timedelta(days=random.randint(*end_date_range))  # Ensure end_date is later
                                    date_values[end_field_name] = end_date

                            except (ValueError, IndexError):
                                raise CommandError(f'Invalid date field definition: {date_field_def}. Use format field_name[,end_field_name]')
                            
                    # Handle time fields with predefined work hours and Django timezone utilities
                    time_values = {}
                    work_hours = [9, 10, 11, 13, 14, 15]  # Example predefined work hours for start time

                    if time_fields:
                        for time_field_def in time_fields:
                            try:
                                parts = time_field_def.split(',')
                                field_name = parts[0]
                                end_field_name = parts[1] if len(parts) > 1 else None

                                # Get the current time using Django's timezone utility
                                current_time = timezone.now()

                                # Randomly select start time from the predefined work hours
                                start_hour = random.choice(work_hours)
                                # Construct start time using timezone-aware current time
                                start_time = current_time.replace(hour=start_hour, minute=0, second=0, microsecond=0).time()
                                time_values[field_name] = start_time

                                # If there's an end time field, set end time 1 or 2 hours after start time
                                if end_field_name:
                                    end_hour = start_hour + random.choice([1, 2])  # Add 1 or 2 hours after start_time
                                    # Construct end time using timezone-aware current time
                                    end_time = current_time.replace(hour=end_hour, minute=0, second=0, microsecond=0).time()
                                    time_values[end_field_name] = end_time

                            except (ValueError, IndexError):
                                raise CommandError(f'Invalid time field definition: {time_field_def}. Use format field_name[,end_field_name]')


                    # Create the main model instance, assigning all foreign keys and date time fields dynamically
                    model.objects.create(
                        **row, # raw data and foreign keys
                        **date_values, # dynamically assign date fields
                        **time_values # dynamically assign time fields
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully created record {idx + 1}'))
        except FileNotFoundError:
            raise CommandError(f'CSV file {csv_file} not found')

