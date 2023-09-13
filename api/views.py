from rest_framework.response import Response
from rest_framework.decorators import api_view
from blogs_app.models import BlogPost
from .serializers import BlogPostSerializer
from django.shortcuts import get_object_or_404
import json

@api_view(['GET'])
def get_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    serializer = BlogPostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def posts(request):
    posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_post(request):
    serializer = BlogPostSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    # вот здесь else будет
    return Response(serializer.data)



    