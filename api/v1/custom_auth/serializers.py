from rest_framework import fields,serializers
# from django.contrib.auth import get_user_model
from api.v1.common.models import User
import re
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','fname','lname','password','business_name','profile_picture','phone_number','is_company']
        extra_kwargs={
            'password':{'write_only':True}

        }
    def create(self, validated_data):
        validated_data['is_company'] = True

        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance       


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
    newPassword = serializers.CharField(min_length=7, write_only=True, required=True)

    def validate_newPassword(self, value):
         if not re.search(r'[a-z]', value):
           raise serializers.ValidationError("Password must contain at least one lowercase letter.")
         if not re.search(r'[0-9]', value):
           raise serializers.ValidationError("Password must contain at least one digit.")
         
         return value