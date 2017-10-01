from django.contrib import admin
from .models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
	
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):

	list_display = ('title', 'slug', 'author', 'publish', 'status')
	list_filter = ('status', 'created', 'publish', 'author')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)
