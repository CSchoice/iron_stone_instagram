from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # 파일이 업로드될 경로를 생성하는 함수
    # 인스턴스는 모델 인스턴스(여기서는 Article)이며, filename은 업로드된 파일의 이름
    # 사용자별로 서브 디렉토리를 생성하여 파일을 저장합니다.

    # 예를 들어, 'media/user_images/username/article_images/filename'와 같은 경로를 반환
    return 'user_images/{0}/article_images/{1}'.format(instance.author.username, filename)


# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_articles'
    )
    updated_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    