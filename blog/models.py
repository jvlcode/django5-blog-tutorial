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
    is_published = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) :
        return self.title
    
    @property
    def formatted_img_url(self):
        if self.img_url:
            # Check if the URL is a full URL
            url = self.img_url if self.img_url.__str__().startswith(('http://', 'https://')) else self.img_url.url
            return url
        return 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'  # Default image UR
    
    class Meta:
        permissions = [
            ("can_publish", "Can publish articles"),
        ]

class AboutUs(models.Model):
    content = models.TextField()

    


