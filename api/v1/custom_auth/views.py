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
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model

# class UserViewset(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
#     queryset = get_user_model().objects.all()

