from rest_framework import fields,serializers
from django.contrib.auth import get_user_model
from . import User
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
