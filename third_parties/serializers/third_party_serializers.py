from openai import NOT_GIVEN
from rest_framework import serializers

from third_parties.services.conversation_analyzer_service import ConversationAnalyzerService
from third_parties.services.speech_to_text_service import SpeechToTextService


class GptMessageSerializer(serializers.Serializer):
    role = serializers.CharField(required=True)
    content = serializers.CharField(required=True)


class ConversationAnalyzerSerializer(serializers.Serializer):
    response = serializers.JSONField(read_only=True)
    model = serializers.CharField(write_only=True, default="gpt-4o-mini")
    messages = serializers.ListSerializer(write_only=True, child=GptMessageSerializer())
    prompt = serializers.ListSerializer(write_only=True, child=GptMessageSerializer())

    dry_run = serializers.BooleanField(default=False, write_only=True)

    def create(self, validated_data):
        dry_run = validated_data.pop("dry_run")
        return ConversationAnalyzerService(validated_data, dry_run).run()


class SpeechToTextSerializer(serializers.Serializer):
    response = serializers.CharField(read_only=True)

    file = serializers.FileField(write_only=True)

    model = serializers.CharField(write_only=True, default="whisper-1")
    language = serializers.CharField(write_only=True, default=NOT_GIVEN)
    prompt = serializers.CharField(write_only=True, default=NOT_GIVEN)
    temperature = serializers.FloatField(write_only=True, default=NOT_GIVEN)

    dry_run = serializers.BooleanField(default=False, write_only=True)

    def create(self, validated_data):
        dry_run = validated_data.pop("dry_run")
        return SpeechToTextService(validated_data, dry_run).run()
