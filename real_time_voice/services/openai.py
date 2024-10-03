from openai import OpenAI


class OpenAIClientProvider:
    client = None

    @classmethod
    def get_openai_client(cls):
        from django.conf import settings
        if cls.client is None:
            cls.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return cls.client
