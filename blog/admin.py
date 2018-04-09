from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from . models import Categorie, BlogPost

# Register your models here.
admin.site.register(Categorie)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "date_created", "category")