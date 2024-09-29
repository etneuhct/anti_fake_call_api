import base64
import logging
import json
import uuid
from pathlib import Path
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from real_time_voice.services import audio
from real_time_voice.services.sms import send_sms
from real_time_voice.services import scam_detection
from real_time_voice.services.transcription import transcribe


HTTP_SERVER_REMOTE_HOST = '84d5-142-113-214-184.ngrok-free.app'

# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent

app_logger = logging.getLogger('app')

class CallingConsumer(WebsocketConsumer):
    def connect(self):
        # self._initialize()
        self.accept()

    def disconnect(self, close_code):
        if len(self.accumulated_stream_bytes) > 0:
            with open(self.mulaw_audio_file, 'wb') as f:
                f.write(self.accumulated_stream_bytes)
                self.accumulated_stream_bytes = bytearray()
            converter = audio.MulawConverter(self.wav_audio_file)
            converter.process_from_file(self.mulaw_audio_file)
            result = transcribe(self.wav_audio_file)
            detection_result = scam_detection.run_detection(result.text)
            app_logger.debug(f'Conversation transcription: {result.text}')
            app_logger.debug(f'Conversation scam detection: {detection_result}')
            if self.fromNumber:
                send_sms(self.fromNumber, f'Sorry I transcribed your conversation: {result.text}\n{detection_result}')

    def calling(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def receive(self, text_data=None, bytes_data=None):
        # self._process_message(text_data)
        pass

    def _initialize(self):
        self.accumulated_stream_bytes = bytearray()
        self.fromNumber = ''
        self.mulaw_audio_file = base_dir / f'audio_conversation_{uuid.uuid4()}'
        self.wav_audio_file = self.mulaw_audio_file.with_suffix('.wav')
        self.message_count = 0
        
        app_logger.debug('Stream URL reached at: {}'.format(self.scope["path"] or 'No URL provided in websocket connection scope.'))

    def _process_message(self, message):
        app_logger.debug("receiving", message)
        data = json.loads(message) if message is not None else None
        if data is None:
            app_logger.info("No message received...")
            return
        if data:
            # Using the event type you can determine what type of message you are receiving
            if data['event'] == "connected":
                app_logger.info("Connected Message received: {}".format(message))
            if data['event'] == "start":
                app_logger.info("Start Message received: {}".format(message))
                fromNumber = data['start']['customParameters'].get('From', '')
                app_logger.debug(f'Called from: {fromNumber}')
            if data['event'] == "media":
                payload = data['media']['payload']
                chunk = base64.b64decode(payload)
                self.accumulated_stream_bytes += chunk
                if not has_seen_media:
                    app_logger.info("Media message: {}".format(message))
                    app_logger.info("Payload is: {}".format(payload))
                    app_logger.info("That's {} bytes".format(len(chunk)))
                    app_logger.info("Additional media messages from WebSocket are being suppressed....")
                    has_seen_media = True
            if data['event'] == "closed":
                app_logger.info("Closed Message received: {}".format(message))
                return
            self.message_count += 1
