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
    path('', views.main_page, name='main_page'),
    path('<int:tar_user_pk>/profile/', views.user_profile, name='user_profile'),
    path('users/<int:user_pk>/followers/', views.get_followers_list, name='get_followers_list'),
    path('users/<int:user_pk>/following/', views.get_following_list, name='get_following_list'),
    path('create/', views.create_article, name='create_article'),
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    path('<int:article_pk>/edit/', views.edit_article, name='edit_article'),
    path('<int:article_pk>/comment/', views.create_comment, name='create_comment'),
    path('<int:article_pk>/comment/<int:comment_pk>/edit/', views.edit_comment, name='edit_comment'),
    path('<int:article_pk>/like/', views.like_article, name='like_article'),
]

