from django.conf import settings


class TwilioService:

    def send_sms(self, destination_phone_number, message, virtual_phone_number=None):
        self.virtual_phone_number = virtual_phone_number \
            if virtual_phone_number \
            else settings.TWILIO_DEFAULT_PHONE_NUMBER

    def associate_user_phone_number_to_virtual_phone_number(self, user_phone_number, virtual_phone_number):
        pass
