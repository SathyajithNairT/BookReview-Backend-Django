from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BookDetails, Review


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    

    def validate(self, data):
        if User.objects.filter(username = data.get('username')).exists():
            return serializers.ValidationError({'username': 'Username already exists.'})
        
        if User.objects.filter(email = data.get('email')).exists():
            return serializers.ValidationError({'email': 'Email already exists.'})
        
        return data 
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email = validated_data['email'],
            password= validated_data['password']
        )

        return user 
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetails
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'userID', 'username', 'bookID', 'review']

    def get_username(self, obj):
        return obj.userID.username

