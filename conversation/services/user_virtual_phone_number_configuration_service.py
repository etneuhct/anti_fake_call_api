from conversation.constants import UserVirtualPhoneNumberStatus
from conversation.models import UserVirtualPhoneNumber


class UserVirtualPhoneNumberConfigurationService:

    def __init__(self, user_virtual_phone_number: UserVirtualPhoneNumber):
        self.user_virtual_phone_number = user_virtual_phone_number

    def run(self):
        UserVirtualPhoneNumber.objects.filter(
            virtual_phone_number=self.user_virtual_phone_number.virtual_phone_number
        ).exclude(id=self.user_virtual_phone_number.id).update(
            status=UserVirtualPhoneNumberStatus.is_inactive
        )
