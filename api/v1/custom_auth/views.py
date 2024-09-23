from django.shortcuts import render
from .serializers import UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework import viewsets
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
from rest_framework import status
from rest_framework.exceptions import Throttled
from django.core import signing
class UserViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

class RegisterCompany(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)   



class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    def post(self, request):
        serializer_email = ForgotPasswordSerializer(data=request.data)
    
        if serializer_email.is_valid():
            email = serializer_email._validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uuid = urlsafe_base64_encode(force_bytes(user.pk))

                signed_data = signing.dumps({'uid' : uuid, 'token' : token})
                send_mail(
                    "Reset your password on property hive"
                    ,f"Please click the link below to change your password: https://propertyhive.com/reset-password?token={signed_data}"
                    , "phive699@gmail.com",
                    [email], 
                    fail_silently=False
                )
                return Response({"message" : "Password reset email sent."}, 
                                status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"message" : "email not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response( serializer_email.errors, status.HTTP_400_BAD_REQUEST)
    
    def throttled(self, request, wait):
        raise Throttled(detail=f"Too many requests. Try again in {int(wait / 60)} min.")



class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    def post(self, request):
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
                    return Response({"message" : "Password has been reset."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Token does not match the user"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"message" : "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
