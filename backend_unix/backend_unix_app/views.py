import asyncio
from multiprocessing import process
import subprocess
import tracemalloc
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from .consumers import LogConsumer
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import UserManager
from .models import UserData
from rest_framework.authtoken.models import Token
from rest_framework import status
from .utils import generate_otp, send_otp_phone
import logging
from django.core.management.base import BaseCommand
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer

from subprocess import PIPE, Popen
from sys import stdout, stdin, stderr
import time, os, signal
from .tasks import execute_command_task


logger = logging.getLogger(__name__)

# Get a logger instance
# logger1 = logging.getLogger(__name__)
logger = logging.getLogger("backend_unix_app")


class RootView(APIView):
    permission_classes = [AllowAny]  # Make it public, accessible by anyone

    def get(self, request):
        return Response({"message": "Welcome to the API!"})


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginWithOTP(APIView):

    def post(self, request):
        # print(request.data)
        if "email" not in request.data:
            return Response(
                {"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        email = request.data.get("email", "")
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        # print(serializer.validated_data)
        logger.info(serializer)
        if serializer.is_valid():
            print(serializer.validated_data)
            try:
                user = UserData.objects.get(email=email)
            except UserData.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            otp = generate_otp()
            user.otp = otp
            user.save()
            phone = "+919080824765"
            send_otp_phone(phone, otp)
            token_data = serializer.validated_data
            # token_data.update({"otp_sent_to": phone})

            logger.info(token_data)
            # send_otp_phone(phone_number, otp)
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # email = request.data.get("email", "")
        # print(email)


class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get("email", "")
        otp = request.data.get("otp", "")
        print(email)
        print(otp)
        logger.info(email)
        try:
            user = UserData.objects.get(email=email)
        except UserData.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        print(type(user.otp))
        print(type(otp))
        if user.otp == int(otp):
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            # token, _ = Token.objects.get_or_create(user=user)

            return Response({"otp": otp}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
            )


class Command(APIView, BaseCommand):
    def post(self, request, *args, **options):
        tracemalloc.start()
        proc_list = []
        form_data = request.data.get("formData", {})
        commands = [
            value for value in form_data.values() if value
        ]  # Keeps only non-empty values

        print(commands)
        snapshot_before = tracemalloc.take_snapshot()
        channel_layer = get_channel_layer()  # Access the channel layer

        for command in commands:
            try:
                # Start the process
                proc = Popen(
                    command,
                    shell=True,
                    stdin=subprocess.PIPE,  # You can set to None if you don't need stdin
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                # Communicate with the process (capture stdout and stderr)
                stdout, stderr = proc.communicate()

                # Handle stdout
                if stdout:
                    output = f"{command} Output: {stdout.decode('utf-8')}"
                    try:
                        # Some business logic
                        logger.info("This is an info log.")

                        # Send log message to WebSocket using channel_layer
                        async_to_sync(channel_layer.group_send)(
                            "logs_group",  # Group name
                            {
                                "type": "send_log",  # Matches the consumer's method name
                                "message": output,
                            },
                        )
                    except Exception as e:
                        async_to_sync(channel_layer.group_send)(
                            "logs_group",
                            {
                                "type": "send_log",
                                "message": f"Error: {e}",
                            },
                        )

                # Handle stderr if any
                if stderr:
                    error_output = f"{command} Error: {stderr.decode('utf-8')}"
                    async_to_sync(channel_layer.group_send)(
                        "logs_group",
                        {
                            "type": "send_log",
                            "message": error_output,
                        },
                    )

                # Append the process to the list
                proc_list.append(proc)

            except Exception as e:
                logger.error(f"Error executing command '{command}': {e}")
                # Handle error case (e.g., WebSocket failure, subprocess error)
                async_to_sync(channel_layer.group_send)(
                    "logs_group",
                    {
                        "type": "send_log",
                        "message": f"Error executing command '{command}': {e}",
                    },
                )

        # Memory usage tracking
        snapshot_after = tracemalloc.take_snapshot()
        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        logger.info("Memory usage comparison (before vs after subprocess execution):")
        for stat in top_stats[:10]:
            logger.info(stat)

        return Response({"message": "Commands executed."}, status=200)


class Commandasync(APIView):
    def post(self, request, *args, **kwargs):
        tracemalloc.start()
        form_data = request.data.get("formData", {})
        commands = [value for value in form_data.values() if value]

        # Snapshot memory usage before
        snapshot_before = tracemalloc.take_snapshot()

        # Trigger Celery tasks for each command
        for command in commands:
            execute_command_task.delay(command)

        # Snapshot memory usage after
        snapshot_after = tracemalloc.take_snapshot()
        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        logger.info("Memory usage comparison (before vs after subprocess execution):")
        for stat in top_stats[:10]:
            logger.info(stat)

        return Response({"message": "Commands are being executed."}, status=200)
