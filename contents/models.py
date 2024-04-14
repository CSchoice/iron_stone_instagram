from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_articles'
    )

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)