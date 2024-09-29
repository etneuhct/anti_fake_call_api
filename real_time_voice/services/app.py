import base64
import json
import logging
from pathlib import Path

from flask import Flask, request
from flask_sockets import Sockets
from werkzeug.routing import Rule
import whisper

import scam_detection
from transcription import transcribe
from audio import MulawConverter
from sms import send_sms


model = whisper.load_model("base")

app = Flask(__name__)
sockets = Sockets(app)

HTTP_SERVER_PORT = 5000
HTTP_SERVER_REMOTE_HOST = '84d5-142-113-214-184.ngrok-free.app'

# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent


@app.route('/start_call', methods=['POST'])
def start_call():
    fromNumber = request.values.get('From', '')
    with open('call.xml', 'r') as f:
        return f.read().replace(
            '{HTTP_SERVER_REMOTE_HOST}', HTTP_SERVER_REMOTE_HOST
        ).replace(
            '{fromNumber}', fromNumber
        )


def echo(ws):
    accumulated_bytes = bytearray()
    fromNumber = ''
    mulaw_audio_file = base_dir / 'audio_conversation'
    wav_audio_file = mulaw_audio_file.with_suffix('.wav')
    print('Stream URL reached at:', request.url)

    print("Connection accepted")
    # A lot of messages will be sent rapidly. We'll stop showing after the first one.
    has_seen_media = False
    message_count = 0
    while not ws.closed:
        message = ws.receive()
        if message is None:
            app.logger.info("No message received...")
            continue

        # Messages are a JSON encoded string
        data = json.loads(message)

        # Using the event type you can determine what type of message you are receiving
        if data['event'] == "connected":
            app.logger.info("Connected Message received: {}".format(message))
        if data['event'] == "start":
            app.logger.info("Start Message received: {}".format(message))
            fromNumber = data['start']['customParameters'].get('From', '')
            print(f'Called from: {fromNumber}')
        if data['event'] == "media":
            payload = data['media']['payload']
            chunk = base64.b64decode(payload)
            accumulated_bytes += chunk
            if not has_seen_media:
                app.logger.info("Media message: {}".format(message))
                app.logger.info("Payload is: {}".format(payload))
                app.logger.info("That's {} bytes".format(len(chunk)))
                app.logger.info("Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "closed":
            app.logger.info("Closed Message received: {}".format(message))
            break
        message_count += 1
    if len(accumulated_bytes):   
        with open(mulaw_audio_file, 'wb') as f:
            f.write(accumulated_bytes)
            accumulated_bytes = bytearray()
        converter = MulawConverter(wav_audio_file)
        converter.process_from_file(mulaw_audio_file)
        result = transcribe(wav_audio_file)
        detection_result = scam_detection.run_detection(result.text)
        print(f'Conversation transcription: {result.text}')
        print(f'Conversation scam detection: {detection_result}')
        if fromNumber:
            send_sms(fromNumber, f'Sorry I transcribed your conversation: {result.text}\n{detection_result}')

    app.logger.info("Connection closed. Received a total of {} messages".format(message_count))

sockets.url_map.add(Rule('/media', endpoint=echo, websocket=True))

if __name__ == '__main__':
    import sys
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    server.serve_forever()
