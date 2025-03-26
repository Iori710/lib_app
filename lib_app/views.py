from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required 
from django.views.generic import View
from django.db.models import Q
from .models import Book, Library
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET

# Create your views here.
class LibRegisterForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['ISBN']
        
class BookRegisterForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['shelf', 'c_code']

def Register(request):
    
    if request.method == 'POST':
        try:
            url = "https://ndlsearch.ndl.go.jp/api/opensearch?isbn=%d" % int(request.POST['ISBN'])  
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                xml_string = response.read().decode('UTF-8')
            root = ET.fromstring(xml_string)
               
        except urllib.error.HTTPError:
           
            return render(request, "lib_app/register.html",
                       {
                            "error_message":"正しく入力されていない、もしくは該当する書籍が存在しません"
                        }
                        )
       ##ここから後で34行目に移動     
        try:
            n_ISBN = Library.objects.get(ISBN = int(request.POST['ISBN']))
            n_ISBN.stock += 1
            n_ISBN.save()    
        
        except:
            n_ISBN = Library(ISBN = int(request.POST['ISBN']))
            n_ISBN.save()
        
        book = Book(
            ISBN = n_ISBN, 
            title = root.find('rss/channel/item/title').text, 
            writer = root.find('rss/channel/item/auther').text,
            publisher = root.find('rss/channel/item/publisher').text,
            shelf = request.POST['shelf'],
            c_code = request.POST['c_code']
        )
        book.save()
        #ここまで34行目に移動
    
    else:
        form1 = LibRegisterForm()
        form2 = BookRegisterForm()
        
    return render(request,"lib_app/register.html",{ "form1":form1, "form2":form2 })
        

@login_required(login_url="/login/")#ログインしていない場合ログイン画面に遷移する
def Top(request):#内容は仮
    book_list = Book.objects.all()
    return render(request, "lib_app/top.html", {'book_list': book_list})

def Logout(request):
    logout(request)
    return redirect('/login/')