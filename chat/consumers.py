import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Thread, Message
from django.db.models import Q

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
                success = await self.update_message_status(message_id, status)
                if success:
                    # Broadcast status update using async pattern
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
        saved_message_id, created_at = await self.save_message(sender_username, receiver_username, message, message_id)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'sender_profile_pic': sender_profile_pic,
                'message_id': saved_message_id,
                'timestamp': created_at.isoformat(),
                'receiver': receiver_username,  # <-- Make sure this is included!
            }
        )

    async def chat_message(self, event):
        # Forward the message to WebSocket
        message_data = {
            'type': event.get('type', 'message'),
            'message': event.get('message'),
            'sender': event.get('sender'),
            'sender_profile_pic': event.get('sender_profile_pic'),
            'message_id': event.get('message_id'),
            'created_at': event.get('timestamp'),
        }
        
        await self.send(text_data=json.dumps(message_data))

        receiver_username = event.get('receiver')  # Extract receiver from the event

        if receiver_username is not None:
            await self.channel_layer.group_send(
                f"notifications_{receiver_username}",
                {
                    "type": "new_message_notification",
                }
            )

    async def status_update(self, event):
        # Forward the status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'message_id': event['message_id'],
            'status': event['status'],
            'sender': event.get('sender')
        }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message_text, message_id=None):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        thread, _ = Thread.objects.get_or_create_personal_thread(sender, receiver)
        msg = Message.objects.create(thread=thread, sender=sender, text=message_text)
        
        # Update thread's last activity
        thread.save(update_fields=['updated_at'])

        return msg.id, msg.created_at  # Return both ID and timestamp

    @database_sync_to_async
    def update_message_status(self, message_id, status):
        try:
            msg = Message.objects.get(id=message_id)
            if status == 'delivered':
                msg.delivered = True
                msg.save(update_fields=['delivered'])
            elif status == 'seen':
                msg.delivered = True
                msg.read = True
                msg.save(update_fields=['delivered', 'read'])
            
            # Since we're in an async consumer, we should use self.channel_layer directly
            # Remove async_to_sync as we're already in an async context
            return True
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def get_unread_count(self, username):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username=username)
        return Message.objects.filter(receiver=user, is_read=False).count()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            f"notifications_{self.scope['user'].username}",
            self.channel_name
        )
        await self.accept()
        
        # Send initial unread count
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': count
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"notifications_{self.scope['user'].username}",
            self.channel_name
        )

    async def notification_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_message_notification(self, event):
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': count,
        }))

    @database_sync_to_async
    def get_unread_count(self):
        user = self.scope['user']
        threads = Thread.objects.filter(users=user)  # <-- changed from participants=user
        return Message.objects.filter(
            thread__in=threads,
            read=False
        ).exclude(sender=user).count()
