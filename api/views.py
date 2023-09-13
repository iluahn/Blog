from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from blogs_app.models import BlogPost
from .serializers import BlogPostSerializer
from django.shortcuts import get_object_or_404
import json

@api_view(['GET'])
def get_post(request, post_id):
    """Получение записи по post_id. Only GET-method"""
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = BlogPostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def posts(request):
    """Получение всех записей. Only GET-method"""
    posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_post(request):
    """Добавление записи. Only POST-method. \
        Проверка валидности заполненных полей проверяется сериалайзером"""
    serializer = BlogPostSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def edit_post(request, post_id):
    """Изменение записи по post_id. При GET-запросе выводит текущую запись\
        для просмотра. При PUT-запросе формирует измененную запись из\
        переданных в request данных и текущих данных (если в request заполнены не все поля)"""
    # пытаемся получить запись по post_id
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # при GET возвращаем текущую запись для просмотра
    if(request.method == 'GET'):
        return Response(BlogPostSerializer(post).data)
    # при PUT берем данные из request и дополняем их значениями текущей записи (если не хватает)
    elif(request.method == 'PUT'):
        new_data = request.data.copy()
        if(not new_data.get('title')):
            new_data['title'] = post.title
        if(not new_data.get('text')):
            new_data['text'] = post.text
        if(not new_data.get('owner')):
            new_data['owner'] = post.owner.id
        # не забыть передать instance, чтобы изменялась текущая запись, а не создавалась новая
        serializer = BlogPostSerializer(instance=post, data=new_data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_post(request, post_id):
    """Удаление записи по post_id. Only DELETE-method"""
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    post.delete()
    return Response({"info": "deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)




    