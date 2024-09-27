from django.conf import settings
from twilio.rest import Client


class TwilioService:

    @staticmethod
    def send_sms(destination_phone_number, message, virtual_phone_number=None):
        virtual_phone_number = virtual_phone_number \
            if virtual_phone_number \
            else settings.TWILIO_DEFAULT_PHONE_NUMBER

        if settings.FORCE_REDIRECT_SMS and settings.FORCE_REDIRECT_SMS_PHONE_NUMBER:
            destination_phone_number = settings.FORCE_REDIRECT_SMS_PHONE_NUMBER

        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        if not settings.DRY_SMS:
            client.messages.create(
                body=message,
                from_=virtual_phone_number,
                to=destination_phone_number,
            )
        else:
            print(message)
