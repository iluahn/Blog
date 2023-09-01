"""URL'S приложения users"""

from django.urls import path, include
from . import views

# определяем namespace для, например, < a href...>
app_name = 'users'
urlpatterns = [
    # Страница с логином
    path('', include('django.contrib.auth.urls')),
    # Страница с регистрацией
    path('register/', views.register, name="register")
]
