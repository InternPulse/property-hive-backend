from django.urls import path, include
from .views import RegisterCompany
urlpatterns=[
    path('register',RegisterCompany.as_view()),
]
