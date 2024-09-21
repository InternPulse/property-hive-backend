"""
User Management API
====================

This API provides endpoints for managing user accounts and profiles,
 allowing for retrieving and updating user information, as well as registering new companies. All endpoints are secured and require authentication tokens.

Classes
-------
1. UserViewset(viewsets.ModelViewSet)
2. RegisterCompany(APIView)
3. UserProfileView(APIView)

Endpoints
---------
1. /users/ [GET, POST, PUT]
   - User Viewset to manage user accounts (Requires authentication).
   
2. /profile/ [GET, PUT]
   - Retrieves and updates the user profile (Requires authentication).

3. /register/company/ [POST]
   - Registers a new company using the provided user data.

Usage
-----
- Token authentication is required for all endpoints except user registration.
- Responses are returned in JSON format with appropriate status codes.
"""

from django.shortcuts import render
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from api.v1.common.models import User

class UserViewset(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving users.

    Methods:
    --------
    - GET: Retrieves all users or a specific user by ID.
    - POST: Creates a new user in the system.
    - PUT: Updates a user's details.

    Authentication:
    ---------------
    Requires token authentication for all requests.

    Permissions:
    ------------
    - IsAuthenticated: Only authenticated users can access these endpoints.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

class RegisterCompany(APIView):
    """
    API endpoint for registering a new company.

    Methods:
    --------
    - POST: Registers a new company with the provided user data (JSON payload).

    Request Body:
    -------------
    - username: str
    - email: str
    - password: str

    Response:
    ---------
    Returns the registered user data upon successful registration.

    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProfileView(APIView):
    """
    API endpoint to retrieve or update the authenticated user's profile.

    Methods:
    --------
    - GET: Retrieves the user's profile data.
    - PUT: Updates the user's profile with provided data (partial updates allowed).

    Authentication:
    ---------------
    Requires token authentication for all requests.

    Permissions:
    ------------
    - IsAuthenticated: Only authenticated users can access these endpoints.

    GET Response:
    -------------
    - statusCode: 200
    - message: Profile retrieved successfully
    - data: Contains user profile data (name, email, phone number, etc.)

    PUT Response:
    --------------
    - statusCode: 200
    - message: Profile updated successfully
    - data: Updated user profile data

    Error Handling:
    ---------------
    Returns 400 for invalid data with the corresponding error message.
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the authenticated user's profile information.

        Request:
        --------
        - Header: Authorization (Token)

        Response:
        ---------
        Returns the user's profile data along with a status message.
        """
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({
            "statusCode": 200,
            "message": "Profile retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update the authenticated user's profile information.

        Request:
        --------
        - Header: Authorization (Token)
        - Body: JSON object containing fields to update (e.g., phone number, identification documents).

        Response:
        ---------
        Returns the updated profile data along with a status message.
        """
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "statusCode": 200,
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
