from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.db.models import Q, Avg
from django.http import Http404, HttpResponse, JsonResponse
from datetime import timedelta, datetime  # 必要に応じてインポート
from functools import reduce
from operator import and_
from .models import Book, Library, Review, Reserve
import urllib.request
import xml.etree.ElementTree as ET
import bootstrap_datepicker_plus.widgets as datetimepicker
import json
import time
from django.urls import reverse

class LibForm(forms.ModelForm):#なぜかforms.pyを作成・インポートしても反応しないのでここに作る
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
        
class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['lending_start', 'lending_end']

class CalendarForm(forms.Form):
    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)

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
def BookReserve(request,ISBN):
    info = Book.objects.filter(ISBN__exact=ISBN)[0]
    return render(request, 'lib_app/reserve.html', {'ISBN':ISBN, 'info':info})

def BookCalendar(request,ISBN):
    if request.method == 'GET':
        raise Http404()
    
    datas = json.loads(request.body)
    
    calendarForm = CalendarForm(datas)
    if not calendarForm.is_valid:
        raise Http404()
    
    start = datas['start_date']
    end = datas['end_date']
    
    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end / 1000))
    
    # 予約情報を取得
    reserve_info = Reserve.objects.filter(
        book_id__ISBN__exact = ISBN,
        lending_start__lte = formatted_end_date,
        lending_end__gte = formatted_start_date
    )

    # 予約情報をJSON形式に変換
    events = []
    for info in reserve_info:
        events.append({
            'title':'予約済み',
            'start': info.lending_start,
            'end': info.lending_end + timedelta(days=1),  # 終了日を1日後に設定
        })

    return JsonResponse(events, safe=False)
    
@login_required
def BookReserving(request, ISBN):  # 予約登録用
    if request.method == 'GET':
        raise Http404()

    datas = json.loads(request.body)

    reserveform = ReserveForm(datas)
    if reserveform.is_valid:
        lending_start = datas['lending_start']
        lending_end = datas['lending_end']
        library = Library.objects.get(ISBN__exact=ISBN)

        formatted_lending_start = time.strftime(
            "%Y-%m-%d", time.localtime(lending_start / 1000))
        formatted_lending_end = time.strftime(
            "%Y-%m-%d", time.localtime(lending_end / 1000))

        # lending_endを1日前に調整
        lending_end_date = datetime.strptime(formatted_lending_end, "%Y-%m-%d")
        adjusted_lending_end = lending_end_date - timedelta(days=1)
        lending_end_date = adjusted_lending_end.strftime("%Y-%m-%d")
        
        # 予約期間中の「既に予約されている冊数」を検索
        reserved_books = Reserve.objects.filter(
            book_id__ISBN__exact = ISBN,
        ).exclude(
            Q(lending_start__gte = lending_end_date)|
            Q(lending_end__lte = formatted_lending_start)
        ).values('book_id')
        
        # 在庫数を超えている場合は予約を拒否
        if  reserved_books.count() >= library.stock:
            raise Http404()
        
        available_books = Book.objects.filter(
            ISBN__exact = ISBN,
        ).exclude(
            id__in = reserved_books
        )
        
        # 最初の貸出可能な書籍を取得
        book_to_reserve = available_books.first()

        reserve = Reserve(
            user_id = request.user,
            book_id = book_to_reserve,
            lending_start = formatted_lending_start,
            lending_end = lending_end_date,  
        )
        reserve.save()

    return HttpResponse("")

@login_required
def BookReserved(request,ISBN):
    info = Reserve.objects.filter(user_id__exact=request.user).order_by('-id')[0] #最新予約を取得
    book = info.book_id
    return render(request, 'lib_app/reserved.html', {'ISBN':ISBN, 'info':info, 'book':book})

def Logout(request):
    logout(request)
    return redirect(reverse('login'))

def Debug(request): #デバッグ用 完成したら消す
    reserved_books = Reserve.objects.filter(
            book_id__ISBN__exact=9784764106871,
        ).exclude(
            Q(lending_start__gte='2025-04-16')|
            Q(lending_end__lte='2025-04-13')
        ).values('book_id')
        
    available_books = Book.objects.filter(
            ISBN__exact=9784764106871,
        ).exclude(
            id__in= '1'
        )
    
    return render(request, 'lib_app/debug.html', {'reserve':reserved_books,'book':available_books}) #最初の貸出可能な書籍を取得