import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        # Use database_sync_to_async for the DB lookup
        self.room = await self.get_room(self.room_slug)
        
        if not self.room:
            await self.close()
            return
        
        self.room_group_name = f"chat_{self.room_slug}"
        self.user = self.scope["user"]

        # Directly await channel layer operations
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_room(self, slug):
        try:
            return Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]
        
        # Save message and render HTML in a separate thread
        html = await self.save_and_render_message(message_text)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": html}
        )

    @database_sync_to_async
    def save_and_render_message(self, content):
        message_obj = Message.objects.create(room=self.room, user=self.user, content=content)
        return render_to_string("partials/message.html", {"message": message_obj})

    async def chat_message(self, event):
        await self.send(text_data=event["message"])