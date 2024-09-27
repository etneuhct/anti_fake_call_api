from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from conversation.models import PhoneNumberVerification
from conversation.serializers.phone_number_verification_serializers import PhoneNumberVerificationCreateSerializer, \
    PhoneNumberVerificationCheckCodeSerializer


class PhoneNumberVerificationViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = PhoneNumberVerificationCheckCodeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = PhoneNumberVerification.objects.filter(user_phone_number__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return PhoneNumberVerificationCreateSerializer
        return super().get_serializer_class()
