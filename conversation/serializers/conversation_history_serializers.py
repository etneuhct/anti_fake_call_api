from conversation.models import ConversationHistory
from rest_framework import serializers

from conversation.serializers.contact_serializers import ContactSerializer
from conversation.serializers.user_virtual_phone_number_serializers import UserVirtualPhoneNumberSerializer


class ConversationHistorySerializer(serializers.ModelSerializer):
    user_virtual_phone_number_detail = UserVirtualPhoneNumberSerializer(source="user_virtual_phone_number")
    contact_detail = ContactSerializer(source="contact")

    class Meta:
        model = ConversationHistory
        fields = (
            "id", "calling_status", "analysis_status", "created_at", "started_at", "ended_at", "conversations",
            "insights", "contact_detail", "user_virtual_phone_number_detail", "user_virtual_phone_number", "contact",)
