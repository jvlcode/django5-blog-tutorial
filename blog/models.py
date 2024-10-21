from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    img_url = models.ImageField(upload_to='posts/images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) :
        return self.title


class AboutUs(models.Model):
    content = models.TextField()

    


