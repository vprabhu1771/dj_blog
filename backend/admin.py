from django.contrib import admin
from backend.models import Tag, Post

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'content')