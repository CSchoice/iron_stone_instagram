"""
URL configuration for instagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


app_name = 'contents'
urlpatterns = [
    path('contents/', views.main_page, name='main_page'),
    path('contents/<int:tar_user_pk>/profile/', views.user_profile, name='user_profile'),
    path('users/<int:user_pk>/followers/', views.get_followers_list, name='get_followers_list'),
    path('users/<int:user_pk>/following/', views.get_following_list, name='get_following_list'),
    path('contents/create/', views.create_article, name='create_article'),
    path('contents/<int:article_pk>/', views.article_detail, name='article_detail'),
    path('contents/<int:article_pk>/update/', views.update_article, name='update_article'),
    path('contents/<int:article_pk>/delete/', views.delete_article, name='delete_article'),
    path('contents/<int:article_pk>/comment_create/', views.create_comment, name='create_comment'),
    path('contents/<int:article_pk>/comment/<int:comment_pk>/update/', views.update_comment, name='update_comment'),
    path('contents/<int:article_pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
    path('contents/<int:article_pk>/like/', views.like_article, name='like_article'),
]

