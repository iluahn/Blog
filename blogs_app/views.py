from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.

def main_page(request):
    """Главная страница (пока что не используется почти)"""
    return render(request, 'blogs_app/main_page.html')

def posts(request):
    """Страница с постами, где осущетсвляется вывод всех постов"""
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'blogs_app/posts.html', context)

@login_required
def new_post(request):
    """Создание нового поста"""
    if(request.method != 'POST'):
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if(form.is_valid()):
            # Не сохраняем в БД, пока не назначен owner
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs_app:posts')
    # возвращаем пустую или неправильную форму
    context = {'form': form}
    return render(request, 'blogs_app/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Редактирование поста"""
    #post = BlogPost.objects.get(id=post_id)
    post = get_object_or_404(BlogPost, id=post_id)
    if(post.owner != request.user):
        raise Http404
    if(request.method != 'POST'):
        form = PostForm(instance=post)
    elif("delete" in request.POST):
        post.delete()
        return redirect('blogs_app:posts')
    elif("save" in request.POST):
        form = PostForm(data=request.POST, instance=post)
        if(form.is_valid()):
            form.save()
            return redirect('blogs_app:posts')
    context = {'form': form, 'post': post}
    # вывод формы, которая содержит сам пост
    return render(request, 'blogs_app/edit_post.html', context)

def custom404(request, exception):
    """Кастомный NOT FOUND"""
    return render(request, 'errors/404.html')

def custom500(request):
    """Кастомная внутренняя ошибка"""
    return render(request, 'errors/500.html')


        

