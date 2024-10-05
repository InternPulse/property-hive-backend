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
from .serializers import UserSerializer, UserProfileSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, CustomerSerializer, EmailVerificationSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from api.v1.common.models import User
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import Throttled
from django.core import signing
from django.utils import timezone


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
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)  # Set is_active to False
        user.generate_verification_code()
        send_mail(
            'Your Verification Code',
            f'Your verification code is {user.email_verification_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
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




class ForgotPasswordView(APIView):
    """
    API endpoint to initiate the password reset process by sending a reset email.

    Methods:
    --------
    - POST: Sends a password reset email to the user if the email is valid.

    Authentication:
    ---------------
    No authentication required.

    Throttling:
    -----------
    - AnonRateThrottle: Restricts the rate of password reset requests for unauthenticated users.

    POST Response:
    --------------
    - statusCode: 200
    - message: Password reset email sent
    - statusCode: 404
    - message: Email not found

    Error Handling:
    ---------------
    Returns 400 for invalid data with the corresponding error message.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        """
        Send a password reset email if the provided email is valid.

        Request:
        --------
        - Body: JSON object containing the user's email.

        Response:
        ---------
        - statusCode: 200 if email is valid and reset email is sent.
        - statusCode: 404 if email is not found in the database.
        """
        serializer_email = ForgotPasswordSerializer(data=request.data)

        if serializer_email.is_valid():
            email = serializer_email.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uuid = urlsafe_base64_encode(force_bytes(user.pk))

                signed_data = signing.dumps({'uid': uuid, 'token': token})
                send_mail(
                    "Reset your password on Property Hive",
                    f"Please click the link below to change your password: https://propertyhive.com/reset-password?token={signed_data}",
                    "phive699@gmail.com",
                    [email],
                    fail_silently=False
                )
                return Response({
                    "message": "Password reset email sent."
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({
                    "message": "Email not found."
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer_email.errors, status=status.HTTP_400_BAD_REQUEST)

    def throttled(self, request, wait):
        """
        Handle throttling errors and provide a user-friendly message.
        """
        raise Throttled(detail=f"Too many requests. Try again in {int(wait / 60)} minutes.")


class ResetPasswordView(APIView):
    """
    API endpoint to reset the user's password using a valid token.

    Methods:
    --------
    - POST: Resets the user's password if the token is valid.

    Authentication:
    ---------------
    No authentication required.

    Throttling:
    -----------
    - AnonRateThrottle: Restricts the rate of password reset requests for unauthenticated users.

    POST Response:
    --------------
    - statusCode: 200
    - message: Password has been reset
    - statusCode: 400
    - message: Token does not match the user or invalid token

    Error Handling:
    ---------------
    Returns 400 for invalid token or password reset errors.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        """
        Reset the user's password if the provided token is valid.

        Request:
        --------
        - Body: JSON object containing the token and new password.

        Response:
        ---------
        - statusCode: 200 if password reset is successful.
        - statusCode: 400 if token is invalid or does not match the user.
        """
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            token_data = serializer.validated_data['token']
            try:
                unsigned_data = signing.loads(token_data)
                uid = urlsafe_base64_decode(unsigned_data.get('uid')).decode()
                token = unsigned_data.get('token')
                user = User.objects.get(id=uid)

                if default_token_generator.check_token(user, token):
                    new_password = serializer.validated_data['newPassword']
                    user.set_password(new_password)
                    user.save()
                    return Response({
                        "message": "Password has been reset."
                    }, status=status.HTTP_200_OK)
                return Response({
                    "message": "Token does not match the user."
                }, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({
                    "message": "Invalid Token."
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def throttled(self, request, wait):
        """
        Handle throttling errors and provide a user-friendly message.
        """
        raise Throttled(detail=f"Too many requests. Try again in {int(wait / 60)} minutes.")


class CustomerView(APIView):
    """
    API endpoint to create a new customer.

    Methods:
    --------
    - POST: Creates a new customer using the provided data.

    Authentication:
    ---------------
    No authentication is required for this endpoint (AllowAny).

    Permissions:
    ------------
    - AllowAny: Anyone can access this endpoint.

    POST Response:
    --------------
    - statusCode: 201
    - message: Customer created successfully
    - data: Contains the newly created customer's data (username, email, etc.)

    Error Handling:
    ---------------
    - Returns 400 for invalid data with a message.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save(is_active=False)  # Set is_active to False
                user.generate_verification_code()
                send_mail(
                    'Your Verification Code',
                    f'Your verification code is {user.email_verification_code}',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                return Response({
                    "message": "Customer created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({
                    "message": "Invalid data"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class SendVerificationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            user.generate_verification_code()
            send_mail(
                'Your Verification Code',
                f'Your verification code is {user.email_verification_code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    return Response({'message': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
                if user.email_verification_code == code and timezone.now() < user.email_verification_expiry:
                    user.email_verification_code = None
                    user.email_verification_expiry = None
                    user.is_active = True
                    user.save()
                    return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)