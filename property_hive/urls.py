from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.company.urls")),
    path("api/v1/", include("api.v1.custom_auth.urls")),
    path("api/v1/", include("api.v1.transaction.urls")),
]
