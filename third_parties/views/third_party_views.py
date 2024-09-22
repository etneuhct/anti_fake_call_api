from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from third_parties.serializers.third_party_serializers import ConversationAnalyzerSerializer, SpeechToTextSerializer
from utils.authentication import ApiKeyAuthentication


class ThirdPartyViewSet(GenericViewSet):
    permission_classes = []
    authentication_classes = [ApiKeyAuthentication]
    parser_classes = [MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.action == "conversation_analyzer":
            return ConversationAnalyzerSerializer
        elif self.action == "speech_to_text":
            return SpeechToTextSerializer
        return super().get_serializer_class()

    @action(methods=("post",), url_name="conversation-analyzer", url_path="conversation-analyzer", detail=False)
    def conversation_analyzer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(methods=("post",), url_name="speech-to-text", url_path="speech-to-text", detail=False)
    def speech_to_text(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
