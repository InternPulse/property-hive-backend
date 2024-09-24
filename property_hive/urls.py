from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

# from api.v1.custom_auth.views import UserViewset
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("api.v1.company.urls")),
    path("api/v1/", include("api.v1.transaction.urls")),
    path("api/v1/", include("api.v1.custom_auth.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# router = DefaultRouter()
# router.register('user',UserViewset ,basename='user')

# urlpatterns += router.urls
