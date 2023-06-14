from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(phone="0966453047").exists():
            User.objects.create_superuser(first_name="Gadisa",last_name="Teka",phone="0966453047", email="admin@gmail.com", password="pass123")
            self.stdout.write(self.style.SUCCESS('Successfully created superuser!'))
        else:
            self.stdout.write(self.style.NOTICE('Superuser already exists.'))

