from django.contrib import admin
from hc.blog.models import Category
from hc.blog.models import Post


admin.site.register(Category)
admin.site.register(Post)