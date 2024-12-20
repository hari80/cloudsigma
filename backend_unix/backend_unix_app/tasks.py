from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import subprocess
import logging

logger = logging.getLogger(__name__)


@shared_task
def execute_command_task(command):
    try:
        # Execute the command synchronously
        process = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Capture stdout and stderr
        stdout = process.stdout.decode("utf-8")
        stderr = process.stderr.decode("utf-8")

        channel_layer = get_channel_layer()
        if stdout:
            message = f"{command} Output: {stdout}"
            async_to_sync(channel_layer.group_send)(
                "logs_group",
                {"type": "send_log", "message": message},
            )
        if stderr:
            message = f"{command} Error: {stderr}"
            async_to_sync(channel_layer.group_send)(
                "logs_group",
                {"type": "send_log", "message": message},
            )
    except Exception as e:
        logger.error(f"Error executing command '{command}': {e}")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "logs_group",
            {
                "type": "send_log",
                "message": f"Error executing command '{command}': {e}",
            },
        )
