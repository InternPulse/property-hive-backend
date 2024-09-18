from django.urls import path
from .views import generate_custom_url

urlpatterns = [
    path(
        "companies/generate-url/",
        generate_custom_url,
        name="generate_custom_url",
    ),
]
