from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .models import RealEstateCompany
from .serializers import RealEstateSerialize
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from ..common.models import User


class RealEstateCompanyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Extract user and business name from request data
        user = request.user

        real_user = User.objects.get(id=user.id)

        if not real_user.is_company:
            print(real_user.is_company)
            return Response(
                {"message": "This is not a company", "status_code": 400},
                status=400,
            )

        company = RealEstateCompany.objects.filter(user=user).first()

        if company:
            return Response(
                {"message": "Company already exists", "status_code": 400},
                status=400,
            )
        base_url = slugify(user.business_name)
        custom_url = f"{base_url}.propertyhive.com"

        real_estate_company = RealEstateCompany.objects.create(
            user=user, custom_url=custom_url
        )

        serializer = RealEstateSerialize(real_estate_company)

        return Response(
            {
                "message": "Custom URL generated successfully",
                "status_code": 201,
                "data": serializer.data,
            },
            status=201,
        )
