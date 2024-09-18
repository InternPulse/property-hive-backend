from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .models import RealEstateCompany
from rest_framework import viewsets


class RealEstateCompanyViewSet(viewsets.ViewSet):
    serializer_class = RealEstateCompany
    queryset = RealEstateCompany.objects.all()

    def create(self, serializer):
        serializer.save()
