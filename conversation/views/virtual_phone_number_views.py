from django.db.models import Q
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conversation.constants import UserVirtualPhoneNumberStatus
from conversation.models import VirtualPhoneNumber
from conversation.serializers.virtual_phone_number_serializers import VirtualPhoneNumberSerializer


class VirtualPhoneNumberViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = VirtualPhoneNumber.objects.filter(
            ~Q(uservirtualphonenumber__status=UserVirtualPhoneNumberStatus.is_active)
        )
        return queryset
