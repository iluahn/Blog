"""Необходим для сериализации объектов модели"""
from rest_framework import serializers
from blogs_app.models import BlogPost
from django.contrib.auth.models import User

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'