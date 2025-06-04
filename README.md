# dj_blog

```
pip install django
```

```
django-admin startproject config .
```

```
python manage.py startapp backend
```

```
python manage.py startapp frontend
```

```
python manage.py runserver
```

```
pip install django-taggit
```

`settings.py`

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'taggit'
]
```

`models.py`

```
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
```