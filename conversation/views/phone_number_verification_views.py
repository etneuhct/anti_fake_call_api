from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from conversation.models import PhoneNumberVerification
from conversation.serializers.phone_number_verification_serializers import PhoneNumberVerificationCreateSerializer, \
    PhoneNumberVerificationCheckCodeSerializer


class PhoneNumberVerificationViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = PhoneNumberVerificationCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = PhoneNumberVerification.objects.filter(user_phone_number__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return PhoneNumberVerificationCreateSerializer
        elif self.action == "check_code":
            return PhoneNumberVerificationCheckCodeSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=("get",), url_path="check-code", url_name="check-code")
    def check_code(self, request, pk):
        data = self.request.query_params
        instance = self.get_object()
        serializer = self.get_serializer(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
