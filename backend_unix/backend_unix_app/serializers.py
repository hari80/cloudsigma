from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from .models import UserData


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")  # Use .get() to avoid KeyError
        if not email:
            raise ValidationError({"email": "This field is required."})

        # Proceed with custom validation
        user = UserData.objects.filter(email=email).first()
        if not user:
            raise ValidationError({"email": "User does not exist."})

        # Generate tokens
        data = super().validate(attrs)
        print(data)
        data.update({"user_id": user.id, "email": user.email})
        # return {"user_id": user.id, "email": user.email}
        return data
