from django.urls import path, include
from .views import (
    UserProfileView,
    RegisterCompany,
    ForgotPasswordView,
    ResetPasswordView,
    CustomerView

)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path('register/company/', RegisterCompany.as_view(), name="register_company"),
    path('register/customer', CustomerView.as_view(), name="register_customer"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

]
