import json
from channels.generic.websocket import AsyncWebsocketConsumer


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_group_name = "logs_group"

        # Join the logs group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the logs group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Method to handle messages sent via the channel layer
    async def send_log(self, event):
        log_message = event["message"]  # Extract the message from the event
        # Send log message to the WebSocket
        await self.send(text_data=json.dumps({"message": log_message}))

    # Helper method to broadcast logs to WebSocket clients
    async def log_to_websocket(self, log_message):
        """
        This method can be called externally to send a log message
        to all WebSocket clients connected to the logs group.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_log",  # This maps to the `send_log` method
                "message": log_message,
            },
        )
