from conversation.constants import UserVirtualPhoneNumberStatus
from conversation.models import UserVirtualPhoneNumber
from conversation.services.twilio_service import TwilioService


class UserVirtualPhoneNumberConfigurationService:

    def __init__(self, user_virtual_phone_number: UserVirtualPhoneNumber):
        self.user_virtual_phone_number = user_virtual_phone_number

    def run(self):
        self._disable_old_user_virtual_phone_numbers()
        self._associate_user_and_virtual_phone_numbers()
        self._complete_configuration()

    def _disable_old_user_virtual_phone_numbers(self):
        UserVirtualPhoneNumber.objects.exclude(id=self.user_virtual_phone_number.id).update(
            status=UserVirtualPhoneNumberStatus.is_inactive
        )

    def _associate_user_and_virtual_phone_numbers(self):
        TwilioService().associate_user_phone_number_to_virtual_phone_number(
            self.user_virtual_phone_number.user_phone_number.phone_number,
            self.user_virtual_phone_number.virtual_phone_number.phone_number
        )

    def _complete_configuration(self):
        self.user_virtual_phone_number.status = UserVirtualPhoneNumberStatus.is_active
        self.user_virtual_phone_number.save()
