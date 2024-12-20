from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserAccount, PasswordResetToken
from django.utils import timezone
from datetime import timedelta
import random


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = UserAccount(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exists.')
        return value

class PasswordResetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist.')
        return value

    def create(self, validated_data):
        email = validated_data['email']
        user = UserAccount.objects.get(email=email)

        # Delete any existing token for the user (optional but prevents clutter)
        PasswordResetToken.objects.filter(user=user).delete()

        # Create a new token with the required fields
        token_instance = PasswordResetToken(user=user)
        token = token_instance.generate_token()

        self.send_reset_email(email, token)
        return token_instance

    def send_reset_email(self, email, token):
        from django.core.mail import send_mail

        send_mail(
            subject="Password Reset Request",
            message=f"Your password reset token is: {token}",
            from_email="nuristanyqais@gmail.com",
            recipient_list=[email],
        )

class PasswordResetTokenVerification(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')
        if not email:
            raise serializers.ValidationError('email field is required')
        if not token:
            raise serializers.ValidationError('token is required')

        try:

            user = UserAccount.objects.get(email=data['email'])
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist')

        user_tokens = PasswordResetToken.objects.filter(user=user)
        token_instance = user_tokens.first()
        
        if not token_instance or not token_instance.verify_token(data['token']):
            raise serializers.ValidationError('Invalid token')

        return data


        



