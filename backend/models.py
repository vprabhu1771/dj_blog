from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"