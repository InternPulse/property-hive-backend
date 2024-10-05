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
from api.v1.common.models import Profile

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
        
        if request.user not in company.viewed_by.all():
            company.views += 1
            company.viewed_by.add(request.user)
            company.save()

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
                {
                    "message": "Invalid data",
                    "errors": serializer.errors,
                    "status_code": 400
                },
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
