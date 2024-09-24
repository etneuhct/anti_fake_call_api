from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conversation.models import Contact
from conversation.serializers.contact_serializers import ContactSerializer, ContactUpdateSerializer


class ContactViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == "update":
            return ContactUpdateSerializer
        return super().get_serializer_class()
