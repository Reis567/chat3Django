import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Room, Message
from django.contrib.auth.models import User

# Função assíncrona para salvar a mensagem no banco de dados
@sync_to_async
def save_message_async(message, username, room_slug):
    try:
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_slug)
        Message.objects.create(user=user, room=room, content=message)
    except User.DoesNotExist:
        print(f"User '{username}' does not exist.")
    except Room.DoesNotExist:
        print(f"Room '{room_slug}' does not exist.")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = self.scope['url_route']['kwargs']['room_slug']
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))

        # Chama a função assíncrona para salvar a mensagem no banco de dados
        await save_message_async(message, username, self.roomGroupName)
