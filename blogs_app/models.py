from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BlogPost(models.Model):
    """Модель поста в блоге"""
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # добавил владельца каждого поста
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.title