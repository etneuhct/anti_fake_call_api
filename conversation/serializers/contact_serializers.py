from rest_framework import serializers

from conversation.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "phone_number", "whitelisted", "user", "first_name", "last_name",)


class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "whitelisted", "first_name", "last_name",)

    def to_representation(self, instance):
        return ContactSerializer().to_representation(instance)
