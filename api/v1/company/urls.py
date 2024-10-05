from django.urls import path, include
from .views import RealEstateCompanyViewSet, LogoutView, CompanyProfileViewSet,DashBoardView
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register(r"companies/generate-url", RealEstateCompanyViewSet, basename="company")


urlpatterns = [
    path("", include(router.urls)),
    path('company-profile/', CompanyProfileViewSet.as_view(), name='view-update-profile'),
    path('dashboard/<int:profile_id>/',DashBoardView.as_view(), name='viewtest'),
    path('log-out', LogoutView.as_view(), name='logout'),


    ]
