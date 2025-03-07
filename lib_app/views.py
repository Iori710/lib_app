from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required 
from django.views.generic import ListView
from django.db.models import Q
from .models import Book

# Create your views here.

@login_required(login_url="/login/")#ログインしていない場合ログイン画面に遷移する
def Top(request):#内容は仮
    book_list = Book.objects.all()
    return render(request, "lib_app/top.html", {'book_list': book_list})

def Logout(request):
    logout(request)
    return redirect('/login/')