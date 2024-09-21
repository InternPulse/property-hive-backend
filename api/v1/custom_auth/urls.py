from django.urls import path, include
from .views import UserProfileView, RegisterCompany

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path('register/', RegisterCompany.as_view(), name="register_company"),
]
