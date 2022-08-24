import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Meeting
from ..accounts.models import User

class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        print('User joined room: ', self.room_group_name)
        
        # Join room group
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
        print('User left')

    # Receive from WebSocket
    async def receive(self, text_data):
        payload = json.loads(text_data)
        action = payload['action']
        print('self.channel_name: ', self.channel_name)

        if action == 'video-offer' or action == 'video-answer':
            receiver_channel_name = payload['message']['receiver_channel_name']
            payload['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type':'sdp_action',    # helper function
                    'payload': payload,     # message
                }
            )
            return
        payload['message']['receiver_channel_name'] = self.channel_name # channel name of current user
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'sdp_action',
                'payload': payload,
            }
        )

    # Receive from room group
    async  def sdp_action(self, event):
        print('Sent action')
        payload = event['payload']
        # Send message to websocket
        await self.send(text_data=json.dumps(
            payload
        ))

    @database_sync_to_async
    def save_message(self, message):
        sender = User.objects.last()
        meeting = Meeting.objects.last()
        # msg = Message.objects.create(sender=sender, meeting=meeting, content=message)
        return True
        