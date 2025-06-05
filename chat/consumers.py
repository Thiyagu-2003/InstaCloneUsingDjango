import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Thread, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']  # e.g. "1_2"
        self.room_group_name = f'chat_{self.room_name}'

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
        msg_type = data.get('type', 'message')

        if msg_type == 'status_update':
            # Handle delivered/seen status update
            message_id = data.get('message_id')
            status = data.get('status')
            if message_id and status in ['delivered', 'seen']:
                await self.update_message_status(message_id, status)
                # Broadcast status update to group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'status_update',
                        'message_id': message_id,
                        'status': status,
                    }
                )
            return

        # Normal message
        message = data.get('message')
        sender_username = data.get('sender')
        receiver_username = data.get('receiver')
        sender_profile_pic = data.get('sender_profile_pic', '/static/default_profile.jpg')
        message_id = data.get('message_id')

        if not message or not sender_username or not receiver_username:
            return  # Invalid data, silently ignore

        # Save the message to DB and get its ID
        saved_message_id = await self.save_message(sender_username, receiver_username, message, message_id)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'sender_profile_pic': sender_profile_pic,
                'message_id': saved_message_id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_profile_pic': event.get('sender_profile_pic', '/static/default_profile.jpg'),
            'message_id': event.get('message_id'),
        }))

    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'message_id': event['message_id'],
            'status': event['status'],
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message_text, message_id=None):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        thread, _ = Thread.objects.get_or_create_personal_thread(sender, receiver)
        msg = Message.objects.create(thread=thread, sender=sender, text=message_text)
        # Optionally, store message_id if you want to match frontend/backend IDs
        return msg.id

    @database_sync_to_async
    def update_message_status(self, message_id, status):
        try:
            msg = Message.objects.get(id=message_id)
            if status == 'delivered':
                msg.delivered = True
            elif status == 'seen':
                msg.seen = True
            msg.save(update_fields=['delivered', 'seen'])
        except Message.DoesNotExist:
            pass
