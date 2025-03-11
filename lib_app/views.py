from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required 
from django.views.generic import ListView
from django.db.models import Q
from .models import Book, Library
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET

# Create your views here.
def Register(request):
    try:
        url = "https://ndlsearch.ndl.go.jp/api/sru?operation=searchRetrieve&query=isbn=%22{}%22".format(request)    
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            xml_string = response.read()
        root = ET.fromstring(xml_string)    
    except urllib.error.HTTPError:
        
        return render(request, "lib_app/register.html",
                      {
                          "error_message":"正しく入力されていない、もしくは該当する書籍が存在しません"
                      }
                      )
        
    new_ISBN = Library(ISBN=request)

@login_required(login_url="/login/")#ログインしていない場合ログイン画面に遷移する
def Top(request):#内容は仮
    book_list = Book.objects.all()
    return render(request, "lib_app/top.html", {'book_list': book_list})

def Logout(request):
    logout(request)
    return redirect('/login/')