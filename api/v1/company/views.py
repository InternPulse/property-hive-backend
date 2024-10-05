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
from .serializers import CompanyProfileSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from api.v1.common.models import Profile,CompanyView,Property
# import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum

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



class CompanyProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        #Retrieve the company profile
        user = request.user


        company = Profile.objects.filter(userid=user).first()

        if not company:
            return Response({"message": "Company not found", "status_code": 404},
                status=404,)

        # company.views += 1
        # company.save()
        today = timezone.now().date()
        company_view, created = CompanyView.objects.get_or_create(profile=company, viewed_on=today)
        company_view.views += 1
        company_view.save()

        serializer = CompanyProfileSerializer(company)

        return Response(
            {
                "message": "Company profile retrieved successfully",
                "status_code": 200,
                "data": serializer.data,
            },
            status=200,
        )


    def put(self, request):
        user = request.user
        company = Profile.objects.filter(userid=user).first()
        serializer = CompanyProfileSerializer(company, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Company profile updated successfully",
                    "status_code": 200,
                    "data": serializer.data,
                },
                status=200,
            )
        else:
            return Response(
                {"message": "Invalid data", "errors": serializer.errors, "status_code": 400},
                status=400,
            )





class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the token associated with the user
            token = Token.objects.get(user=request.user)
            token.delete()  # Delete the token to log the user out
            return Response({
                "statusCode": 200,
                "message": "Logged out successfully"
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({
                "statusCode": 400,
                "message": "Token does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)






class DashBoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        try:
            company = Profile.objects.get(id=profile_id)

        except Profile.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)


        # Fetch views for the past 7 days
        today = timezone.now().date()
        last_week = today - timedelta(days=7)

        views_per_day = (
            CompanyView.objects.filter(profile=company, viewed_on__gte=last_week)
            .values('viewed_on')
            .annotate(total_views=Sum('views'))
        )
        seller = company.userid
        # Fetch total listings, active listings, and sold properties
        total_listings = Property.objects.filter(sellerid=seller).count()  # All listings by this company
        active_listings = Property.objects.filter(sellerid=seller, is_sold=False).count()  # Active listings
        sold_properties = Property.objects.filter(sellerid=seller, is_sold=True).count()  # Sold properties

        # Return the chart data along with property stats
        return Response({
            "timestamp": [view['viewed_on'] for view in views_per_day],
            "profile_views": [view['total_views'] for view in views_per_day],
            "total_listings": total_listings,
            "active_listings": active_listings,
            "sold_properties": sold_properties
        })
