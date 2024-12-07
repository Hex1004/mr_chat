import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Set the group name (can be dynamically assigned per user/chat)
        self.room_group_name = "group_chat_gfg"

        # Join the chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse the received message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json.get("username", "Unknown")

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_message",
                "message": message,
                "username": username,
            }
        )

    # This method is used to send the message to WebSocket clients
    async def send_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))
