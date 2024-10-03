import base64
import logging
import json
import uuid
from pathlib import Path

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from real_time_voice.services import audio
from real_time_voice.services.sms import send_sms
from real_time_voice.services import scam_detection
from real_time_voice.services.transcription import transcribe
from conversation.services import twilio_conversation_service
import conversation.constants as conversation_constants


# Get the parent directory as a Path object
base_dir = Path(__file__).resolve().parent

app_logger = logging.getLogger('app')


class CallingConsumer(WebsocketConsumer):
    def connect(self):
        self._initialize()
        self.accept()

    def disconnect(self, close_code):
        # analyze conversation and notify user
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
            if self.conversation_entry is not None:
                analysis_status = conversation_constants.ConversationHistoryAnalysisStatus.scam if detection_result['is_scammy'] else conversation_constants.ConversationHistoryAnalysisStatus.is_ok
                calling_status = conversation_constants.ConversationHistoryCallingStatus.bot_hang_up
                twilio_conversation_service.TwilioConversationService.update_conversation(self.conversation_entry.id,
                                                                                           analysis_status=analysis_status,
                                                                                           calling_status=calling_status,
                                                                                           insights_data=detection_result,
                                                                                           transcription_data={'transcription': result.text})
                formatted_call_time = self.conversation_entry.created_at.strftime("%I:%M %p on %A, %b %d, %Y")
                if not detection_result['is_scammy']:
                    sms_text = f'''Hey, this is your Anti-Fake Call protection. You just got a legitimate call from {self.incoming_phone_number} at {formatted_call_time}.
                    We don\'t yet support forwarding legitimate calls as part of this demo. Feel free to call them back at your earliest convenience.
                    Here's our analysis of the call: "{detection_result['explanation']}"'''
                else:
                    sms_text = f'''Hey, this is your Anti-Fake Call protection. We believe you just got a scam call from {self.incoming_phone_number} at {formatted_call_time}.
                    Here's our analysis of the call: "{detection_result['explanation']}"'''
                user_phone_number = twilio_conversation_service.TwilioConversationService.get_user_phone_number_from_conversation(self.conversation_entry.id)
                send_sms(user_phone_number, sms_text)


    def calling(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def receive(self, text_data=None, bytes_data=None):
        try:
            self._process_message(text_data)
        except Exception as e:
            app_logger.error(e)
            self.close()

    def _initialize(self):
        self.has_seen_media = False
        self.accumulated_stream_bytes = bytearray()
        self.incoming_phone_number = ''
        self.conversation_entry = None
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
            if data['event'] == "connected":
                app_logger.info("Connected Message received: {}".format(message))
            if data['event'] == "start":
                app_logger.info("Start Message received: {}".format(message))
                self.incoming_phone_number = data['start']['customParameters'].get('From', '')
                virtual_phone_number = data['start']['customParameters'].get('VirtualNumber', '')
                app_logger.debug(f'Call from: {self.incoming_phone_number}')
                app_logger.debug(f'Call to virtual phone: {virtual_phone_number}')
                if not self.incoming_phone_number:
                    raise Exception('The calling phone number is missing from the request.')
                if not virtual_phone_number:
                    raise Exception('The called virtual phone number is missing from the request.')
                conversation_id = uuid.uuid4()
                self.conversation_entry = twilio_conversation_service.TwilioConversationService.create_conversation_history(conversation_id, virtual_phone_number, self.incoming_phone_number)
            if data['event'] == "media":
                payload = data['media']['payload']
                chunk = base64.b64decode(payload)
                self.accumulated_stream_bytes += chunk

                if not self.has_seen_media:
                    app_logger.info("Media message: {}".format(message))
                    app_logger.info("Payload is: {}".format(payload))
                    app_logger.info("That's {} bytes".format(len(chunk)))
                    app_logger.info("Additional media messages from WebSocket are being suppressed....")
                    self.has_see_media = True
            if data['event'] == "closed":
                app_logger.info("Closed Message received: {}".format(message))
                return
            self.message_count += 1
