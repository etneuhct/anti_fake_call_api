from conversation.models import ConversationHistory
from rest_framework import serializers


class ConversationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationHistory
        fields = (
            "id", "calling_status", "analysis_status", "created_at", "started_at", "ended_at", "conversations",
            "insights",
            "user_virtual_phone_number", "contact",)
