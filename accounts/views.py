from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import UserAccount
from .serializers import UserAccountSerializer
from .serializers import PasswordResetTokenSerializer, PasswordResetTokenVerification




class UserRegistrationView(CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer



class PasswordResetTokenView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetTokenSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.save()
            return Response(
                {"message": "Password reset token has been sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetTokenVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetTokenVerification(data=request.data)
        if serializer.is_valid():
            return Response(
                {'message': 'Email and token has been verified successfully.'},status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

