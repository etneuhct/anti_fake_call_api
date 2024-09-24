from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conversation.models import UserVirtualPhoneNumber
from conversation.serializers.user_virtual_phone_number_serializers import UserVirtualPhoneNumberCreateSerializer, \
    UserVirtualPhoneNumberSerializer


class UserVirtualPhoneNumberViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    serializer_class = UserVirtualPhoneNumberSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = UserVirtualPhoneNumber.objects.filter(user_phone_number__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return UserVirtualPhoneNumberCreateSerializer
        return super().get_serializer_class()
