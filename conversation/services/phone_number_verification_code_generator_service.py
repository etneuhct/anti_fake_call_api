from conversation.models import UserPhoneNumber, PhoneNumberVerification


class PhoneNumberVerificationCodeGeneratorService:
    def __init__(self, user_phone_number: UserPhoneNumber):
        self.user_phone_number = user_phone_number

    def run(self) -> PhoneNumberVerification:
        pass
