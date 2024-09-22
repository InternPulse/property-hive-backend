from django.urls import path, include
from .views import RegisterCompany, ForgotPasswordView, ResetPasswordView
urlpatterns=[
    path('register',RegisterCompany.as_view()),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
]
