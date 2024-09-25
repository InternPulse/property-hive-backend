from django.urls import path, include
from .views import (
    UserProfileView,
    RegisterCompany,
    ForgotPasswordView,
    ResetPasswordView,
    UserViewSet,
    RegisterUserView,
    ProtectedView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path('register/company/', RegisterCompany.as_view(), name="register_company"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    # Additional user management routes
    path('api/v1/property-hive/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/property-hive/register/', RegisterUserView.as_view(), name='register'),  
    path('api/v1/property-hive/protected/', ProtectedView.as_view(), name='protected'),
    path('api/v1/property-hive/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
