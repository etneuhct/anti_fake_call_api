from pathlib import Path

from django.http import HttpResponse

# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent
template_file = base_dir / 'call.xml'

with open(template_file, 'r') as f:
        template_response = f.read()

def incoming_voice_call(request):
    """Handles a call to our Twilio-managed phone number by sending directives to stream the call to a server endpoint."""
    fromNumber = request.GET.get('From', '')
    server_host = request.get_host()
    return HttpResponse(template_response.replace(
        '{HTTP_SERVER_REMOTE_HOST}', server_host
    ).replace(
        '{fromNumber}', fromNumber
    ))
