from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from api.v1.custom_auth.views import UserViewset
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/", include("api.v1.company.urls")),
    path("api/v1/", include("api.v1.custom_auth.urls")),
    # path("api/v1/", include("api.v1.transaction.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# router = DefaultRouter()
#router.register('api/v1/register',UserViewset ,basename='api/v1/register')

# urlpatterns += router.urls
