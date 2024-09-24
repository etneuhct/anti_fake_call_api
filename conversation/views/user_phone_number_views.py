from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conversation.models import UserPhoneNumber
from conversation.serializers.user_phone_number_serializers import UserPhoneNumberCreateSerializer, \
    UserPhoneNumberSerializer


class UserPhoneNumberViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                             mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = UserPhoneNumberSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = UserPhoneNumber.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return UserPhoneNumberCreateSerializer
        return super().get_serializer_class()
