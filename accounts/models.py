from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def user_directory_path(instance, filename):
    # 파일이 업로드될 경로를 생성하는 함수
    # 인스턴스는 모델 인스턴스(여기서는 User)이며, filename은 업로드된 파일의 이름
    # 여기서는 유저별로 서브 디렉토리를 생성하여 파일을 저장

    # 예를 들어, 'media/user_images/username/profile_img/filename'과 같은 경로를 반환
    return 'user_images/{0}/profile_img/{1}'.format(instance.username, filename)

class User(AbstractUser):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    introduce = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to=user_directory_path, blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
