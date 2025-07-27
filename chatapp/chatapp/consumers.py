import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
import datetime

@sync_to_async
def save_message(from_user_id, to_user_id, message):
    from_user = User.objects.get(id=from_user_id)
    to_user = User.objects.get(id=to_user_id)
    chat = ChatMessage.objects.create(from_user=from_user, to_user=to_user, message=message)
    return {
        'id': chat.id,
        'from_user': from_user.get_full_name(),
        'from_user_id': from_user.id,
        'to_user_id': to_user.id,
        'message': chat.message,
        'time': chat.created_at.strftime("%b %d, %H:%M")
    }

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        other_user_id = self.scope['url_route']['kwargs']['user_id']

        print("Connecting user:", user)
        if not user.is_authenticated:
            await self.close()
            return

        # Create consistent room name based on sorted user IDs
        ids = sorted([str(user.id), str(other_user_id)])
        self.room_group_name = f'chat_{ids[0]}_{ids[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data.get('message')
        from_user_id = data.get('from_user_id')
        to_user_id = data.get('to_user_id')

        saved_message = await save_message(from_user_id, to_user_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                **saved_message  # send all message data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
