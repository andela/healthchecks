from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Categorie, BlogPost

# Create your views here.


@login_required
def index(request):
    page = 'blog'
    posts = BlogPost.objects.all()
    context = {"posts": posts, "page":page}
    return render(request, "blog/blog.html", context)

@login_required
def blog_body(request, post_id): 
    post = BlogPost.objects.get(id=post_id)
    context  = {"post": post}
    return render(request, "blog/blog_body.html", context)
