from django.urls import path, include
from .views import UserProfileView, RegisterCompany, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path('register/', RegisterCompany.as_view(), name="register_company"),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
]
