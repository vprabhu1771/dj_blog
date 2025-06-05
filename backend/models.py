from django.db import models
from taggit.managers import TaggableManager

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager


# Create your models here.

class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')

class GenderedImageField(models.ImageField):

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not value or not hasattr(model_instance, self.attname):
            # If no image provided or new instance
            # default gender
            gender = model_instance.gender if hasattr(model_instance, 'gender') else Gender.MALE
            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                # fallback default image
                value = 'profile/default_image.jpg'

        elif model_instance.gender != getattr(model_instance, f"{self.attname}_gender_cache", None):
            # If gender has changed
            gender = model_instance.gender
            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                # fallback default image
                value = 'profile/default_image.jpg'
        setattr(model_instance, f"{self.attname}_gender_cache", model_instance.gender)
        return value


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE)
    image = GenderedImageField(upload_to='profile/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class AuthorUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Author'
        verbose_name_plural= 'Authors'

class MemberUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

class AdminUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table="category"

class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table="tag"


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=255)

    content = models.TextField()

    tags = models.ManyToManyField(Tag, through='PostTag')

    categories = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_tag'
        unique_together = ('post', 'tag')  # Optional: prevent duplicate entries

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_category'
        unique_together = ('post', 'category')  # Optional: prevent duplicate entries