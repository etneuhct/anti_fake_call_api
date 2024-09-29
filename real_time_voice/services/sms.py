import logging
import os

from twilio.rest import Client
from django.conf import settings


app_logger = logging.getLogger('app')

def send_sms(to: str, text: str):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=text,
        from_="+13437006109",
        to=to,
    )
    app_logger.debug(f'sent text message: {message.body}')
