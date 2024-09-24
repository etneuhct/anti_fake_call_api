from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from conversation.services.data_generator import DataGenerator

UserModel = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = UserModel.objects.first()
        DataGenerator(user).run()
