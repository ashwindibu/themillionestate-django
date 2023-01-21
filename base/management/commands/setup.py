from django.core.management import call_command
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating Table, could take upto 5 min'))
        call_command('makemigrations')
        call_command('migrate')

        self.stdout.write(self.style.SUCCESS('Table created successfully'))
        self.stdout.write(self.style.SUCCESS('Running Basic Setup'))
        progress_bar = tqdm(desc="Processing", total=1)

        self.stdout.write(self.style.SUCCESS('Data added successfully'))
        progress_bar.close()
