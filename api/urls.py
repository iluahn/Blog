"""URL'S для api"""

from django.urls import path, include
from . import views

# определяем namespace для, например, < a href 'app:method_name'...>
app_name = 'api'
urlpatterns = [
    # получение всех постов
    path('posts/', views.posts, name='posts'),
    # получение поста
    path('posts/<int:post_id>/', views.get_post, name='get_post'),
    # добавление поста
    path('add/', views.add_post, name='add_post'),
    # редактирование поста
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    # удаление поста
    path('delete/<int:post_id>/', views.delete_post, name="delete_post")
    ]
