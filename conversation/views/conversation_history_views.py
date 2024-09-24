from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conversation.models import ConversationHistory
from conversation.serializers.conversation_history_serializers import ConversationHistorySerializer


class ConversationHistoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = ConversationHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = ConversationHistory.objects.filter(
            user_virtual_phone_number__user_phone_number__user=self.request.user)
        return queryset
