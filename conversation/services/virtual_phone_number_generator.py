from django.utils.timezone import now
from django.conf import settings

from conversation.models import VirtualPhoneNumber


class VirtualPhoneNumberGenerator:

    def run(self):
        twilio_phone_number = settings.TWILIO_DEFAULT_PHONE_NUMBER
        if not twilio_phone_number:
            raise Exception('"TWILIO_DEFAULT_PHONE_NUMBER" is not defined or invalid.')
        # Generate VirtualPhoneNumber if doesn't exist
        virtual_phone_number_record = VirtualPhoneNumber.objects.filter(phone_number=twilio_phone_number).first()
        if virtual_phone_number_record is None:
            virtual_phone_number_record = VirtualPhoneNumber.objects.create(
                phone_number=twilio_phone_number,
                is_active=True,
                created_at=now()
            )
        return virtual_phone_number_record
