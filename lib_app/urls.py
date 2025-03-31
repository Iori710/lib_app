"""
URL configuration for library project.

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
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/',
        LoginView.as_view(
            redirect_authenticated_user = True,
            template_name = "lib_app/login.html",
            next_page = '/top/'
        ),
         name='login'),
    
    path('top/', views.Top, name='top'),
    
    path('logout/', views.Logout, name='logout'),
    
    path('register/', views.Register, name='register'),
    
    path('search/', views.Search, name='search'),
    
    path('mypage/', views.Mypage, name='mypage'),
    
    path('debug/', views.Debug, name='debug'),
    
    path('detail/<int:ISBN>', views.Detail, name='detail'),
]
