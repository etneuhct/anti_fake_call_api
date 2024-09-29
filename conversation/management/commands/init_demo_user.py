from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        UserModel.objects.create_user(
            email=settings.DEMO_USER_EMAIL,
            username=settings.DEMO_USER_EMAIL,
            password=settings.DEMO_USER_PASSWORD,
            first_name="Alex",
            last_name="NoName"
        )
