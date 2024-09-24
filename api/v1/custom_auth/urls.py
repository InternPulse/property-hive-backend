from django.urls import path
from .views import UserViewSet  # Ensure you're importing the correct view
from .views import User  
from .views import (
    RegisterUserView,
    ProtectedView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path('api/v1/property-hive/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/property-hive/register/', RegisterUserView.as_view(), name='register'),  # Added comma here
    path('api/v1/property-hive/protected/', ProtectedView.as_view(), name='protected'),
    path('api/v1/property-hive/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
]
