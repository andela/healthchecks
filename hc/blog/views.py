from django.shortcuts import render
from django.views.generic import ListView
from . import models

class BlogIndex(ListView):
    queryset = models.Entry.object.published()
    template_name = 'front/blog.html'
    context_object_name = 'blog_entries'
    
