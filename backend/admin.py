from django.contrib import admin
from backend.models import Tag, Post, PostTag, Category, PostCategory


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

class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # Number of empty rows shown
    # autocomplete_fields = ['tag']  # Optional: if you have many tags

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'content', 'display_tags', 'display_categories',)

    inlines = [PostTagInline, PostCategoryInline]  # Adds the tabular inline for PostTag

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = 'Tags'

    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

    display_categories.short_description = 'Categories'