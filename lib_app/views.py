from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.views.generic import View
from django.db.models import Q
from functools import reduce
from operator import and_
from .models import Book, Library
from urllib import error
import urllib.request
import xml.etree.ElementTree as ET


# Create your views here.
class LibForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['ISBN']
        
class BookRegisterForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['shelf', 'c_code']
        
class BookSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'writer', 'publisher']

def Register(request):
    form1 = LibForm()
    form2 = BookRegisterForm()
    
    if request.method == 'POST':
        try:
            url = 'https://ndlsearch.ndl.go.jp/api/opensearch?isbn=%d' % int(request.POST['ISBN'])  
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                xml_string = response.read().decode('UTF-8')
            root = ET.fromstring(xml_string)
            
            try:
                n_ISBN = Library.objects.get(ISBN = int(request.POST['ISBN']))
                n_ISBN.stock += 1
                n_ISBN.save()    
        
            except:
                n_ISBN = Library(ISBN = int(request.POST['ISBN']))
                n_ISBN.save()
        
            try:
                book = Book(
                    ISBN = n_ISBN, 
                    title = root.find('channel/item/title').text, 
                    writer = root.find('channel/item/{http://purl.org/dc/elements/1.1/}creator').text.replace(',',' '),
                    publisher = root.find('channel/item/{http://purl.org/dc/elements/1.1/}publisher').text,
                    shelf = request.POST['shelf'],
                    c_code = request.POST['c_code']
                    )
                book.save()
            except:
                book = Book(
                    ISBN = n_ISBN, 
                    title = root.find('channel/item/title').text, 
                    writer = root.find('channel/item/author').text.replace('著',' '),
                    publisher = root.find('channel/item/{http://purl.org/dc/elements/1.1/}publisher').text,
                    shelf = request.POST['shelf'],
                    c_code = request.POST['c_code']
                    )
                book.save() 
            
        except:
            return render(request, 'lib_app/register.html',
                       {
                            'message':'正しく入力されていない、もしくは該当する書籍が存在しません',
                            'form1':form1,
                            'form2':form2
                        }
                        )
        return render(request, 'lib_app/register.html',
                       {
                            'message':'登録しました',
                            'form1':form1,
                            'form2':form2
                        }
                        )
    
    else:    
        return render(request,'lib_app/register.html',{ 'form1':form1, 'form2':form2 })
        

@login_required#ログインしていない場合ログイン画面に遷移する
def Top(request):#内容は仮
    user = request.user
    form1 = BookSearchForm()
    form2 = LibForm()
    return render(request, 'lib_app/top.html', { 'user':user, 'form1':form1, 'form2':form2 })

@login_required
def Mypage(request):
    user = request.user
    return render(request,'lib_app/mypage.html', { 'user':user })

@login_required
def Search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', '　'])
            q_list = ''
            
            for i in keyword:
                if i in exclusion_list:
                    pass
                else:
                    q_list += i
                
        query = reduce(
            and_,[
                Q(title__icontains=q)|
                Q(writer__icontains=q)|
                Q(publisher__icontains=q) for q in q_list]
            )        
        result = Book.objects.filter(query).order_by('title').distinct('title')
        return render(request, 'lib_app/search.html', { 'result':result, 'keyword':keyword })
    else:    
        return redirect('/top/')

@login_required    
def Detail(request,ISBN):
    return render(request, 'lib_app/detail.html', {'ISBN':ISBN})

def Logout(request):
    logout(request)
    return redirect('/login/')

def Debug(request):
    form1 = LibForm()
    form2 = BookRegisterForm()
    
    if request.method == 'POST':
        try:
            url = 'https://ndlsearch.ndl.go.jp/api/opensearch?isbn=%d' % int(request.POST['ISBN'])  
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                xml_string = response.read().decode('UTF-8')
            root = ET.fromstring(xml_string)
               
        except error.HTTPError:
            return render(request, 'lib_app/register.html',
                       {
                            'message':'正しく入力されていない、もしくは該当する書籍が存在しません',
                            'form1':form1,
                            'form2':form2
                        }
                        )
         
        title = root.find('channel/item/title').text 
        writer = root.find('channel/item/{http://purl.org/dc/elements/1.1/}creator').text.replace(',',' ')
        publisher = root.find('channel/item/{http://purl.org/dc/elements/1.1/}publisher').text
        shelf = request.POST['shelf']
        c_code = request.POST['c_code']
        debug = [title, writer, publisher, shelf, c_code]
        return render(request, 'lib_app/debug.html', {'form1':form1, 'form2':form2, 'debug':debug})
    else:    
        return render(request,'lib_app/debug.html',{ 'form1':form1, 'form2':form2 })