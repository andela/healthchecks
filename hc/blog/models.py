from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    
    def __str__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, {'slug': self.slug})
 
 
class Post(models.Model):
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True)
    
    def __str__(self):
        return self.title
    
    
    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, {'slug': self.slug})