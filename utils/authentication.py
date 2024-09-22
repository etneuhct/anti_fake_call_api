from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('API-Key')
        if not api_key or api_key != settings.API_KEY:
            raise AuthenticationFailed('Invalid or missing API Key')
        return None, None
