import random

from django.utils.timezone import now

from conversation.constants import UserVirtualPhoneNumberStatus, ConversationHistoryCallingStatus, \
    ConversationHistoryAnalysisStatus
from conversation.models import VirtualPhoneNumber, UserPhoneNumber, Contact, UserVirtualPhoneNumber, \
    ConversationHistory, PhoneNumberVerification


class DataGenerator:
    def __init__(self, user):
        self.user = user

    def run(self):
        # Generate VirtualPhoneNumber
        virtual_phone_number = VirtualPhoneNumber.objects.create(
            phone_number=f"+123456{random.randint(1000, 9999)}",
            is_active=True,
            created_at=now()
        )

        # Generate UserPhoneNumber
        user_phone_number = UserPhoneNumber.objects.create(
            phone_number=f"+987654{random.randint(1000, 9999)}",
            verified=True,
            created_at=now(),
            user=self.user
        )

        # Generate Contact
        contact = Contact.objects.create(
            phone_number=f"+112233{random.randint(1000, 9999)}",
            whitelisted=False,
            first_name="John",
            last_name="Doe",
            user=self.user
        )

        # Generate UserVirtualPhoneNumber
        user_virtual_phone_number = UserVirtualPhoneNumber.objects.create(
            status=UserVirtualPhoneNumberStatus.pending,
            created_at=now(),
            user_phone_number=user_phone_number,
            virtual_phone_number=virtual_phone_number
        )

        # Generate ConversationHistory
        conversation_history = ConversationHistory.objects.create(
            calling_status=ConversationHistoryCallingStatus.pending,
            analysis_status=ConversationHistoryAnalysisStatus.pending,
            created_at=now(),
            started_at=now(),
            ended_at=now(),
            conversations=[{"message": "Hello", "timestamp": str(now())}],
            insights=[{"summary": "Call completed"}],
            user_virtual_phone_number=user_virtual_phone_number,
            contact=contact
        )

        # Generate PhoneNumberVerification
        phone_number_verification = PhoneNumberVerification.objects.create(
            user_phone_number=user_phone_number,
            code=str(random.randint(100000, 999999)),
            created_at=now()
        )
