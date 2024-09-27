from rest_framework import serializers

from conversation.models import UserPhoneNumber


class UserPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoneNumber
        fields = ("id", "phone_number", "verified", "created_at", "user",)


class UserPhoneNumberCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), allow_null=True
    )

    class Meta:
        model = UserPhoneNumber
        fields = ("id", "phone_number", "created_at", "user",)

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        return UserPhoneNumberSerializer().to_representation(instance)
