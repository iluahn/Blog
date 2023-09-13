"""Необходим для сериализации объектов модели"""
from rest_framework import serializers
from blogs_app.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'