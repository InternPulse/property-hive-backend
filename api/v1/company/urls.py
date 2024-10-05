from django.urls import path, include
from .views import RealEstateCompanyViewSet, LogoutView, CompanyProfileViewSet,DashBoardView
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register(r"companies/generate-url", RealEstateCompanyViewSet, basename="company")


urlpatterns = [
    path("", include(router.urls)),
    path('company-profile/', CompanyProfileViewSet.as_view(), name='view-update-profile'),
    path('dashboard/',DashBoardView.as_view(), name='dashboard'),
    path('log-out', LogoutView.as_view(), name='logout'),


    ]
