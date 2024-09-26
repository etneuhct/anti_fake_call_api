import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CallingConsumer(WebsocketConsumer):
    def connect(self):
        room = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'calling_{room}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def calling(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def receive(self, text_data=None, bytes_data=None):
        print("calling", text_data)
