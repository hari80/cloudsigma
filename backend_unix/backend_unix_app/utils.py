import random
import string
from django.conf import settings
from twilio.rest import Client  # Import the Twilio Client if using Twilio


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_phone(phone_number, otp):
    account_sid = (
        "AC9e1ff018aa2a59a88b80fa902897c01a"  # Replace with your Twilio account SID
    )
    auth_token = (
        "e7337ad7947b7dac58f661679cfe8d06"  # Replace with your Twilio auth token
    )
    twilio_phone_number = "+12182923025"  # Replace with your Twilio phone number

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your OTP is: {otp}", from_=twilio_phone_number, to=phone_number
    )
