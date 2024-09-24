from conversation.models import VirtualPhoneNumber
from rest_framework import serializers


class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ("id", "phone_number", "is_active")
