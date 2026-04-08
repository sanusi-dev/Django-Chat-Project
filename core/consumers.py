import json

from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from .models import Room, Message
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room = self.get_room()
        if not self.room:
            self.close()
            return
        
        self.room_group_name = f"chat_{self.room.slug}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.user = self.scope["user"]
        self.accept()

    def get_room(self):
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        try:
            return Room.objects.get(slug=self.room_slug)
        except Room.DoesNotExist:
            return None

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_obj = Message.objects.create(room=self.room, user=self.user, content=message)
        context = {"message": message_obj}
        text_data = render_to_string("partials/message.html", context)
        # self.send(text_data=text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": text_data}
        )

    def chat_message(self, event):
        self.send(text_data=event["message"])