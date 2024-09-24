from rest_framework import serializers

from conversation.models import PhoneNumberVerification, UserPhoneNumber
from conversation.services.phone_number_verification_code_check_service import PhoneNumberVerificationCodeCheckService
from conversation.services.phone_number_verification_code_generator_service import \
    PhoneNumberVerificationCodeGeneratorService
from utils.primary_key_related_field import GenericUserPrimaryKeyRelatedField


class PhoneNumberVerificationCreateSerializer(serializers.ModelSerializer):
    user_phone_number = GenericUserPrimaryKeyRelatedField(
        queryset=UserPhoneNumber.objects.filter(verified=False)
    )

    class Meta:
        model = PhoneNumberVerification
        fields = ("id", "user_phone_number",)

    def create(self, validated_data):
        user_phone_number = validated_data["user_phone_number"]
        return PhoneNumberVerificationCodeGeneratorService(user_phone_number).run()


class PhoneNumberVerificationCheckCodeSerializer(serializers.ModelSerializer):
    user_phone_number = GenericUserPrimaryKeyRelatedField(
        queryset=UserPhoneNumber.objects.filter(verified=False)
    )
    completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = PhoneNumberVerification
        fields = ("id", "user_phone_number", "code", "completed")

    def update(self, instance, validated_data):
        code = validated_data["code"]
        is_ok = PhoneNumberVerificationCodeCheckService(instance, code).run()
        return {
            "completed": is_ok
        }
