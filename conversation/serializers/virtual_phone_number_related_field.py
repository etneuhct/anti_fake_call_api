from django.db.models import Q
from rest_framework import serializers

from conversation.constants import UserVirtualPhoneNumberStatus
from conversation.models import VirtualPhoneNumber


class VirtualPhoneNumberRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return VirtualPhoneNumber.objects.filter(
            ~Q(uservirtualphonenumber__status=UserVirtualPhoneNumberStatus.is_active)
        )
