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
from .views import *

urlpatterns = [
    path('login/',
        LoginView.as_view(
            redirect_authenticated_user = True,
            template_name = "lib_app/login.html",
            next_page = '/top/'
        ),
         name='login'),
    
    path('logout/', Logout, name='logout'),
    
    path('debug/', Debug, name='debug'),
    
    path('register/', Register, name='register'),
    
    path('top/', Top, name='top'),
    
    path('news/', NewsList, name='news_list'),
    
    path('news/<int:id>', NewsPage, name='news'),
    
    path('search/', Search, name='search'),
    
    path('detail/<int:ISBN>/', Detail, name='detail'),
    
    path('review/<int:ISBN>/', BookReview, name='review'),
    
    path('calendar/<int:ISBN>/', BookCalendar, name='calendar'),
    
    path('reserve/<int:ISBN>/', BookReserve, name='reserve'),
    
    path('reserving/<int:ISBN>/', BookReserving, name='reserving'),

    path('reserved/<int:ISBN>/', BookReserved, name='reserved'),
    
    path('check/',Check, name='check'),
    
    path('lending/', BookLending, name='lending'),
    
    path('returned/', BookReturned, name='returned'),
    
    path('reviewing/<int:ISBN>/', Reviewing, name='reviewing'),
    
    path('mypage/', Mypage, name='mypage'),
    
    path('view/reserve/', ReserveView, name='reserve_view'),
    
    path('view/lending/', LendingView, name='lending_view'),
    
    path('option/', UserOption, name='option'),
    
    path('option/username/', UserNameChange, name='username'),
    
    path('option/password/', PasswordChange, name='password'),
    
    path('contact/', ContactForms, name='contact'),
]
