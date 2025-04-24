from webbrowser import register

from django.contrib import admin

from backend.models import Category, Post, Comment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    # search_fields = ('name',)
#
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at']

    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Comment)