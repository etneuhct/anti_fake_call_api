from pathlib import Path

from django.http import HttpResponse

# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent
template_file = base_dir / 'call.xml'

with open(template_file, 'r') as f:
        template_response = f.read()

def incoming_voice_call(request):
    """Handles a call to our Twilio-managed phone number by sending directives to stream the call to a server endpoint."""
    from django.conf import settings
    fromNumber = request.GET.get('From', '')
    ws_server_url = settings.TWILIO_STREAM_RECEIVER_URL or f'wss://{request.get_host()}/ws'
    return HttpResponse(template_response.replace(
        '{WS_SERVER_URL}', ws_server_url
    ).replace(
        '{fromNumber}', fromNumber
    ))
