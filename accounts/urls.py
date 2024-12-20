from django.urls import path
from .views import UserRegistrationView, PasswordResetTokenView, PasswordResetTokenVerificationView


urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/password-reset/', PasswordResetTokenView.as_view(), name='password-reset'),
    path('users/password-verify/', PasswordResetTokenVerificationView.as_view(), name='password-verify'),
    
    
]