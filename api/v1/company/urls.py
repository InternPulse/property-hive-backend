from django.urls import path
from .views import RealEstateCompanyViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()

router.register(r"generate-url", RealEstateCompanyViewSet, basename="company")
