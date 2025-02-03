from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['username', 'password', 'user_type', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

# serializers.py
from django.contrib.auth.models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'user_type', 'phone']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.user_type = validated_data['user_type']
        user.phone = validated_data['phone']
        user.save()
        return user



class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = '__all__'
# class LandSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Land
#         fields  = '__all__'

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields  = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields  = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields  = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields  = '__all__'