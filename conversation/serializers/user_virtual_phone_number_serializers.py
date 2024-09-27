from rest_framework import serializers

from conversation.models import UserVirtualPhoneNumber, UserPhoneNumber
from conversation.serializers.user_phone_number_serializers import UserPhoneNumberSerializer
from conversation.serializers.virtual_phone_number_related_field import VirtualPhoneNumberRelatedField
from conversation.serializers.virtual_phone_number_serializers import VirtualPhoneNumberSerializer
from conversation.services.user_virtual_phone_number_configuration_service import \
    UserVirtualPhoneNumberConfigurationService
from utils.primary_key_related_field import GenericUserPrimaryKeyRelatedField


class UserVirtualPhoneNumberSerializer(serializers.ModelSerializer):
    virtual_phone_number_detail = VirtualPhoneNumberSerializer(source="virtual_phone_number")
    user_phone_number_detail = UserPhoneNumberSerializer(source="user_phone_number")

    class Meta:
        model = UserVirtualPhoneNumber
        fields = (
            "id", "status", "created_at", "user_phone_number", "virtual_phone_number",
            "user_phone_number_detail", "virtual_phone_number_detail",
        )


class UserVirtualPhoneNumberCreateSerializer(serializers.ModelSerializer):
    user_phone_number = GenericUserPrimaryKeyRelatedField(queryset=UserPhoneNumber.objects.filter(verified=True))
    virtual_phone_number = VirtualPhoneNumberRelatedField()

    class Meta:
        model = UserVirtualPhoneNumber
        fields = ("id", "user_phone_number", "virtual_phone_number")

    def create(self, validated_data):
        instance = super().create(validated_data)
        UserVirtualPhoneNumberConfigurationService(instance).run()
        return instance

    def to_representation(self, instance):
        return UserVirtualPhoneNumberSerializer().to_representation(instance)


class UserVirtualPhoneNumberUpdateSerializer(serializers.ModelSerializer):
    user_phone_number = GenericUserPrimaryKeyRelatedField(queryset=UserPhoneNumber.objects.filter(verified=True))

    class Meta:
        model = UserVirtualPhoneNumber
        fields = ("id", "user_phone_number")

    def to_representation(self, instance):
        return UserVirtualPhoneNumberSerializer().to_representation(instance)
