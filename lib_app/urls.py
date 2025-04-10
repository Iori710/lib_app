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
    
    path('logout/', views.Logout, name='logout'),
    
    path('debug/', views.Debug, name='debug'),
    
    path('register/', views.Register, name='register'),
    
    path('top/', views.Top, name='top'),
    
    path('news/', views.NewsList, name='news_list'),
    
    path('news/<int:id>', views.NewsPage, name='news'),
    
    path('search/', views.Search, name='search'),
    
    path('detail/<int:ISBN>/', views.Detail, name='detail'),
    
    path('review/<int:ISBN>/', views.BookReview, name='review'),
    
    path('calendar/<int:ISBN>/', views.BookCalendar, name='calendar'),
    
    path('reserve/<int:ISBN>/', views.BookReserve, name='reserve'),
    
    path('reserving/<int:ISBN>/', views.BookReserving, name='reserving'),

    path('reserved/<int:ISBN>/', views.BookReserved, name='reserved'),
    
    path('check/',views.Check, name='check'),
    
    path('lending/', views.BookLending, name='lending'),
    
    path('returned/', views.BookReturned, name='returned'),
    
    path('reviewing/<int:ISBN>/', views.Reviewing, name='reviewing'),
    
    path('mypage/', views.Mypage, name='mypage'),
    
    path('view/reserve/', views.ReserveView, name='reserve_view'),
    
    path('view/lending/', views.LendingView, name='lending_view'),
    
    path('option/', views.UserOption, name='option'),
    
    path('option/username/', views.UserNameChange, name='username'),
    
    path('option/password/', views.PasswordChange, name='password'),
    
    path('contact/', views.ContactForms, name='contact'),
]
