"""URL'S приложения blogs_app"""

from django.urls import path, include
from . import views

# определяем namespace для, например, < a href 'app:method_name'...>
app_name = 'blogs_app'
urlpatterns = [
    # Главная страница
    path('', views.main_page, name='main_page'),
    # Страница с постами
    path('posts/', views.posts, name='posts'),
    # Страница с созданием нового поста
    path('new_post/', views.new_post, name='new_post'),
    # Страница с редактированием поста
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]
