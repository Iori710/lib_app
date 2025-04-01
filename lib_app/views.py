from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.db.models import Q, Avg
from functools import reduce
from operator import and_
from .models import Book, Library, Review
import urllib.request
import xml.etree.ElementTree as ET

#なぜかforms.pyを作成・インポートしても反応しないのでここに作る
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

# Create your views here.
def Register(request):
    form1 = LibForm()
    form2 = BookRegisterForm()
    
    if request.method == 'POST':
        try: #APIからXMLデータを取得して読み込む
            url = 'https://ndlsearch.ndl.go.jp/api/opensearch?isbn=%d' % int(request.POST['ISBN'])  
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                xml_string = response.read().decode('UTF-8')
            root = ET.fromstring(xml_string)
            
            try: #既に同じ書籍があるなら在庫データを増やす
                n_ISBN = Library.objects.get(ISBN = int(request.POST['ISBN']))
                n_ISBN.stock += 1
                n_ISBN.save()    
        
            except: #ないならデータを作る
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
            except: #↑のwriter部分が存在しないXMLファイルもあったため用意
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
        #「夏目漱石　人」のように空白を用いて複数検索できるようにする
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
    info = Book.objects.filter(ISBN__exact=ISBN)[0]
    review = Review.objects.filter(ISBN__exact=ISBN).order_by('-id')[:3] #最新レビュー3件のみ表示
    return render(request, 'lib_app/detail.html', {'ISBN':ISBN, 'info':info, 'review':review})

@login_required
def BookReview(request,ISBN):
    title = Book.objects.filter(ISBN__exact=ISBN)[0].title
    review = Review.objects.filter(ISBN__exact=ISBN).order_by('-id')
    average = review.aggregate(Avg('stars')).get('stars__avg')
    return render(request, 'lib_app/review.html', {'title':title, 'review':review, 'average':average, 'ISBN':ISBN})

@login_required
def Reserve(request,ISBN):
    return

def Logout(request):
    logout(request)
    return redirect('/login/')

def Debug(request): #デバッグ用 完成したら消す
    form1 = LibForm()
    form2 = BookRegisterForm()