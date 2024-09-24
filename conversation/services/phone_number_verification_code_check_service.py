from conversation.models import PhoneNumberVerification


class PhoneNumberVerificationCodeCheckService:
    def __init__(self, phone_number_verification: PhoneNumberVerification, code):
        self.phone_number_verification = phone_number_verification

    def run(self) -> bool:
        return True
