from django.urls import path, include
from .views import (
    UserProfileView,
    RegisterCompany,
    ForgotPasswordView,
    ResetPasswordView,
    CustomerView,
    SendVerificationEmailView,
    VerifyEmailView,
    CustomerLoginView,
    CompanyLoginView
)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path('login/company', CompanyLoginView.as_view(), name="company_login"),
    path('login/customer', CustomerLoginView.as_view(), name="customer_login"),
    path('register/company/', RegisterCompany.as_view(), name="register_company"),
    path('register/customer', CustomerView.as_view(), name="register_customer"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('send-verification-email/', SendVerificationEmailView.as_view(), name='send_verification_email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

]
