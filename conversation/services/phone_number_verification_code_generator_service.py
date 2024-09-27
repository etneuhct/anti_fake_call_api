import random
import string

from conversation.models import UserPhoneNumber, PhoneNumberVerification
from conversation.services.twilio_service import TwilioService


class PhoneNumberVerificationCodeGeneratorService:
    def __init__(self, user_phone_number: UserPhoneNumber):
        self.user_phone_number = user_phone_number

    def run(self) -> PhoneNumberVerification:
        code = self._generate_code()
        message = code

        PhoneNumberVerification.objects.filter(
            user_phone_number=self.user_phone_number
        ).delete()

        instance = PhoneNumberVerification.objects.create(
            code=code,
            user_phone_number=self.user_phone_number
        )
        TwilioService.send_sms(instance.user_phone_number.phone_number, message)

        return instance

    @staticmethod
    def _generate_code():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    @staticmethod
    def _generate_message(code):
        return code
