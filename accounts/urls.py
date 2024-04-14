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

app_name = 'accounts'
urlpatterns = [
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/logout/', views.user_logout, name='user_logout'),
    path('contents/<int:user_pk>/update/', views.update_user_profile, name='update_user_profile'),
    path('accounts/<int:tar_user_pk>/follow/', views.follow_user, name='follow_user'),
]
