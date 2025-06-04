from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
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