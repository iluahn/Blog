from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from blogs_app.models import BlogPost
from .serializers import BlogPostSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import json

@api_view(['GET'])
def get_routes(request):
    """Вывод информации о существующих маршрутах"""
    routes = {
        'api/signup/': "signup in system",
        'api/token/obtain/': "get access- and refresh-token by given valid username and password",
        'api/token/refresh/': "refresh access-token by given valid refresh-token",
        'api/posts/': "get all posts (no authorization required)",
        'api/post/{post_id}': "get post by post_id (no authorization required)",
        'api/add/': "add post ('Authorization': 'Bearer {access-token}' should be included in the HTTP header)",
        'api/edit/{post_id}': "edit post by post_id ('Authorization': 'Bearer {access-token}' should be included in the HTTP header)",
        'api/delete/{post_id}': "delete post by post_id ('Authorization': 'Bearer {access-token}' should be included in the HTTP header)",
    }
    return Response(routes)

@api_view(['POST', 'GET'])
def signup(request):
    """Регистрация пользователя. Валидность заполненных полей проверяется сериалайзером"""
    if(request.method == 'GET'):
        return Response({"info": "'username' and 'password' fields are required"})
    serializer = UserSerializer(data=request.data)
    if(not serializer.is_valid()):
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    user = User.objects.get(username=serializer.data['username'])
    # хэшируем пароль, а затем сохраняем обновленный пароль в БД
    user.set_password(user.password)
    user.save()
    return Response({"info": f"user {user.username} succesfully created!"}, status=status.HTTP_201_CREATED)

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
#@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_post(request):
    """Добавление записи. Only POST-method. \
        Валидность заполненных полей проверяется сериалайзером"""
    serializer = BlogPostSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def edit_post(request, post_id):
    """Изменение записи по post_id (изменение доступно только владельцу записи). При GET-запросе\
        выводит текущую запись для просмотра. При PUT-запросе формирует измененную запись из\
        переданных в request данных и текущих данных (если в request заполнены не все поля)"""
    # пытаемся получить запись по post_id
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # поскольку используются function-based views, сделать отдельный кастомный permission
    # с has_object_permission на проверку owner'а не получится, нужно писать явно
    if(post.owner != request.user):
        raise PermissionDenied("Only post's owner can edit post!")

    # при GET возвращаем текущую запись для просмотра
    if(request.method == 'GET'):
        return Response(BlogPostSerializer(post).data)
    # при PUT берем данные из request и дополняем их значениями текущей записи (если не хватает)
    elif(request.method == 'PUT'):
        new_data = request.data.copy()
        if(new_data.get('title') is None):
            new_data['title'] = post.title
        if(new_data.get('text') is None):
            new_data['text'] = post.text
        if(new_data.get('owner') is None):
            new_data['owner'] = post.owner.id
        # не забыть передать instance, чтобы изменялась текущая запись, а не создавалась новая
        serializer = BlogPostSerializer(instance=post, data=new_data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    """Удаление записи по post_id (доступно только владельцу записи). Only DELETE-method"""
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # поскольку используются function-based views, сделать отдельный кастомный permission
    # с has_object_permission на проверку owner'а не получится, нужно писать явно
    if(post.owner != request.user):
        raise PermissionDenied("Only post's owner can delete post!")

    post.delete()
    return Response({"info": "deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)




    