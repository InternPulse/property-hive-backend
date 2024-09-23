from django.urls import path, include
from .views import RealEstateCompanyViewSet, LogoutView, CompanyProfileViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register(r"companies/generate-url", RealEstateCompanyViewSet, basename="company")


urlpatterns = [
    path("", include(router.urls)),
    path('/profile', CompanyProfileViewSet.as_view(), name='view-update-profile'),
    path('/log-out', LogoutView.as_view(), name='logout'),


    ]
