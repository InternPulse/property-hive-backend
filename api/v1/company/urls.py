from django.urls import path, include
from .views import RealEstateCompanyViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"companies/generate-url", RealEstateCompanyViewSet, basename="company")


urlpatterns = [path("", include(router.urls))]
