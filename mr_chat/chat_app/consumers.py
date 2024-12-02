import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.channel = None

    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Corrected to use `channel_layer`
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
            })

    async def sendMessage(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

