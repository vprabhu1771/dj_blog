from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from backend.forms import CustomUserCreationForm, CustomUserChangeForm
from backend.models import Tag, Post, PostTag, Category, PostCategory, AuthorUser, MemberUser, AdminUser


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

class BaseCustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email','gender','image_tag','is_staff','is_active',)
    list_filter = ('email','is_staff','is_active',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None,{'fields':('email','gender','password','groups')}),
        ('Permissions',{'fields':('is_staff','is_active')}),
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('email','gender','password1','password2','is_staff','is_active',)
        })
    )

    def image_tag(self,obj):
        if obj.image:
            return format_html('<img src="{}"width="50" height="50" />', obj.image.url)
        return "-"

    image_tag.short_description = 'Image'

# Filter users by group or role (adjust logic if using roles instead of groups)
@admin.register(AuthorUser)
class AuthorAdmin(BaseCustomUserAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(groups__name='Author')

@admin.register(MemberUser)
class MemberAdmin(BaseCustomUserAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(groups__name='Member')

@admin.register(AdminUser)
class AdminUserAdmin(BaseCustomUserAdmin):
    def get_queryset(self,request):
        return super().get_queryset(request).filter(groups__name='Admin')