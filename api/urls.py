"""URL'S для api"""

from django.urls import path, include
from rest_framework.authtoken import views as token_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# определяем namespace для, например, < a href 'app:method_name'...>
app_name = 'api'
urlpatterns = [
    # выводим доступные маршруты
    path('', views.get_routes, name="get_routes"),
    # регистрация
    path('signup/', views.signup, name = "signup"),
    # получение всех постов
    path('posts/', views.posts, name='posts'),
    # получение поста
    path('posts/<int:post_id>/', views.get_post, name='get_post'),
    # добавление поста
    path('add/', views.add_post, name='add_post'),
    # редактирование поста
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    # удаление поста
    path('delete/<int:post_id>/', views.delete_post, name="delete_post"),
    # авторизация и получение токена
    path('token/obtain/', TokenObtainPairView.as_view(), name="token_obtain"),
    # обновление access-токена по refresh-токену
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]
