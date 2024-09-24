from rest_framework import serializers

from conversation.models import UserVirtualPhoneNumber, UserPhoneNumber
from conversation.serializers.virtual_phone_number_related_field import VirtualPhoneNumberRelatedField
from utils.primary_key_related_field import GenericUserPrimaryKeyRelatedField


class UserVirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVirtualPhoneNumber
        fields = (
            "id", "status", "created_at", "user_phone_number", "virtual_phone_number",
        )


class UserVirtualPhoneNumberCreateSerializer(serializers.ModelSerializer):
    user_phone_number = GenericUserPrimaryKeyRelatedField(queryset=UserPhoneNumber.objects.filter(verified=True))
    virtual_phone_number = VirtualPhoneNumberRelatedField()

    class Meta:
        model = UserVirtualPhoneNumber
        fields = ("id", "user_phone_number", "virtual_phone_number")

    def to_representation(self, instance):
        return UserVirtualPhoneNumberSerializer().to_representation(instance)
