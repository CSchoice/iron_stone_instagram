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
from .views import LoginView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('<int:user_pk>/control/', views.update_user_profile, name='update_user_profile'),
    path('<int:tar_user_pk>/follow/', views.follow_user, name='follow_user'),
    path('api/token/', obtain_auth_token, name='token_obtain_pair'),
    path('check_login', views.check_login, name='check_login'),
]
