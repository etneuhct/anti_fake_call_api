from conversation.models import PhoneNumberVerification


class PhoneNumberVerificationCodeCheckService:
    def __init__(self, phone_number_verification: PhoneNumberVerification, code):
        self.phone_number_verification = phone_number_verification
        self.code = code

    def run(self) -> bool:
        is_ok = self.code == self.phone_number_verification.code
        user_phone_number = self.phone_number_verification.user_phone_number
        if is_ok:
            user_phone_number.verified = is_ok
            PhoneNumberVerification.objects.filter(user_phone_number=user_phone_number).delete()
        return is_ok
