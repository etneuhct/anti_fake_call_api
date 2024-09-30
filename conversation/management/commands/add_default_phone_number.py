from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from conversation.services.virtual_phone_number_generator import VirtualPhoneNumberGenerator

UserModel = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        virtual_phone_number_record = VirtualPhoneNumberGenerator().run()
        print(f'This virtual phone number has been saved to database: {virtual_phone_number_record.phone_number}.')
