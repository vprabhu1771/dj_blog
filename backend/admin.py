from django.contrib import admin
from backend.models import Tag, Post, PostTag, Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('name',)

class PostTagInline(admin.TabularInline):
    model = PostTag
    extra = 1  # Number of empty rows shown
    # autocomplete_fields = ['tag']  # Optional: if you have many tags

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'content', 'display_tags',)

    inlines = [PostTagInline]  # Adds the tabular inline for PostTag

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = 'Tags'