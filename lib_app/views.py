from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm 
from django.db.models import Q, Avg
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from datetime import timedelta, datetime
from functools import reduce
from operator import and_
from .models import *
import urllib.request
import xml.etree.ElementTree as ET
import json
import time
from .forms import *

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
                            'book':book,
                            'form1':form1,
                            'form2':form2
                        }
                        )
    
    else:    
        return render(request,'lib_app/register.html',{ 'form1':form1, 'form2':form2 })        

@login_required#ログインしていない場合ログイン画面に遷移する
def Top(request):
    user = request.user
    news = News.objects.all().order_by('-id')[:3] #最新ニュース3件のみ表示
    
    lending = Lending.objects.all()
    message1 = ''
    message2 = ''
    if Reserve.objects.filter(
        user_id__exact=user, 
        lending_start__lte=datetime.now()
    ).exclude(id__in=lending.values('id')).exists(): #貸出可能な書籍がある場合
        message1 = '貸出できる書籍があります'
    
    if lending.filter(
        user_id__exact=user,
        lending_end__exact=datetime.now() + timedelta(days=1), 
        returned=False
    ).exists(): #返却日が明日の書籍がある場合
        message2 = '明日が返却日の書籍があります'
    elif lending.filter(
        user_id__exact=user,
        lending_end__exact=datetime.now(), 
        returned=False
    ).exists(): #返却日が今日の書籍がある場合
        message2 = '本日が返却日の書籍があります'
    elif lending.filter(
        user_id__exact=user,
        lending_end__lte=datetime.now(), 
        returned=False
    ).exists(): #返却日が過ぎている書籍がある場合
        message2 = '返却日が過ぎている書籍があります 速やかに返却してください'
    
    return render(request, 'lib_app/top.html', { 'user':user, 'news':news, 'message1':message1, 'message2':message2 })

@login_required
def NewsList(request):
    news = News.objects.all().order_by('-id') #全ニュースを取得
    return render(request, 'lib_app/news_list.html', { 'news':news })

@login_required
def NewsPage(request, id):
    news = News.objects.get(id__exact=id)
    return render(request, 'lib_app/news.html', { 'news':news })

@login_required
def Mypage(request):
    user = request.user
    return render(request,'lib_app/mypage.html', { 'user':user })

@login_required
def ContactForms(request):
    form = ContactForm()
    if request.method == 'POST':
        contact = Contact(
            user_id = request.user,
            message = request.POST['message']
        )
        contact.save()
        return render(request, 'lib_app/contact.html', {'form':form, 'message':'お問い合わせ内容を送信しました'})
    else:
        return render(request, 'lib_app/contact.html', {'form': form})

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
        
        else:
            return redirect('/top/')
                
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
    info = Book.objects.filter(ISBN__exact=ISBN).first()
    review = Review.objects.filter(ISBN__exact=ISBN).order_by('-id')[:3] #最新レビュー3件のみ表示
    return render(request, 'lib_app/detail.html', {'ISBN':ISBN, 'info':info, 'review':review})

@login_required
def BookReview(request,ISBN):
    title = Book.objects.filter(ISBN__exact=ISBN).first().title
    review = Review.objects.filter(ISBN__exact=ISBN).order_by('-id')
    average = review.aggregate(Avg('stars')).get('stars__avg')
    return render(request, 'lib_app/review.html', {'title':title, 'review':review, 'average':average, 'ISBN':ISBN})

@login_required
def BookReserve(request,ISBN):
    info = Book.objects.filter(ISBN__exact=ISBN).first()
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
    ).exclude(id__in=Lending.objects.filter(returned=True).values('book_id')) #貸出中の書籍は除外

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
def BookReserving(request, ISBN):
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
        lending_end_date_1 = adjusted_lending_end.strftime("%Y-%m-%d")
        
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
            lending_end = lending_end_date_1,  
        )
        reserve.save()

    return HttpResponse("")

@login_required
def BookReserved(request,ISBN):
    info = Reserve.objects.filter(user_id__exact=request.user).order_by('-id').first() #最新予約を取得
    book = info.book_id
    return render(request, 'lib_app/reserved.html', {'ISBN':ISBN, 'info':info, 'book':book})

@login_required
def Check(request):

    if request.method == 'POST':
        c_code = request.POST['keyword']
        try:
            returned_book = Lending.objects.get(
                book_id__c_code__exact = c_code, returned = False
            )
            request.session['returned_book_id'] = returned_book.id
            return redirect(reverse('returned'))
        except Lending.DoesNotExist:
            try:
                lending_book = Reserve.objects.filter(
                    book_id__c_code__exact = c_code,
                    user_id__exact=request.user,
                    lending_start__lte = datetime.now()
                ).exclude(lending_end__lt = datetime.now()).first()
                
                #セッションにデータ保存
                request.session['lending_book_id'] = lending_book.id
                return redirect(reverse('lending'))
            except:
                return render(request, 'lib_app/check.html', {'message': '正しく入力されていない、もしくは貸出日になっていません'})
    else:
        return render(request, 'lib_app/check.html')

@login_required
def BookReturned(request):
    id_ = request.session.get('returned_book_id')
    returned_book = get_object_or_404(Lending, id__exact=id_)
    if request.method =='POST':
        returned_book.returned = True
        returned_book.save()
        
        Reserve.objects.get(id__exact=id_).delete() #予約データ削除
        
        isbn = returned_book.book_id.ISBN
        title = returned_book.book_id.title
        writer = returned_book.book_id.writer
        #セッションからデータ削除
        del request.session['returned_book_id']
        
        return render(request, 'lib_app/returned.html', {
            'returned_book':returned_book, 'ISBN':isbn, 'title':title, 'writer':writer
        })  
    else:
        isbn = returned_book.book_id.ISBN
        title = returned_book.book_id.title
        writer = returned_book.book_id.writer        
        return render(request, 'lib_app/returned_check.html', {
            'returned_book':returned_book, 'ISBN':isbn, 'title':title, 'writer':writer
        })

@login_required
def BookLending(request):
    id_ = request.session.get('lending_book_id')
    lending_book = get_object_or_404(Reserve, id__exact=id_)
    if request.method =='POST':
        lend_book = Lending(
            user_id = request.user,
            book_id = lending_book.book_id,
            lending_start = lending_book.lending_start,
            lending_end = lending_book.lending_end,
            returned = False
        )   
        lend_book.save()
        lending_book.delete() #予約データ削除
        
        isbn = lend_book.book_id.ISBN
        title = lend_book.book_id.title
        writer = lend_book.book_id.writer
        #セッションからデータ削除
        del request.session['lending_book_id']
        
        return render(request, 'lib_app/lending.html', {
            'lending_book':lend_book, 'ISBN':isbn, 'title':title, 'writer':writer
            })  
    else:
        isbn = lending_book.book_id.ISBN
        title = lending_book.book_id.title
        writer = lending_book.book_id.writer   
        return render(request, 'lib_app/lending_check.html', {
            'lending_book':lending_book, 'ISBN':isbn, 'title':title, 'writer':writer
        })

@login_required
def Reviewing(request,ISBN):
    title = Book.objects.filter(ISBN__exact=ISBN).first().title
    if request.method == 'POST':
        reviews = Review(
            user_id = request.user,
            ISBN = Library.objects.get(ISBN__exact=ISBN),
            stars = request.POST['stars'],
            review = request.POST['review']
        )
        reviews.save()
        
        return render(request, 'lib_app/reviewing_ty.html',{'ISBN':ISBN, 'title':title})
    else:
        form = ReviewForm()
        return render(request, 'lib_app/reviewing.html',{'ISBN':ISBN, 'form':form, 'title':title})

@login_required
def ReserveView(request):
    lending = Lending.objects.all().values('id')
    reserve = Reserve.objects.filter(user_id__exact=request.user, lending_start__gte = datetime.now()).exclude(id__in=lending)
    if reserve.count() == 0:
        return render(request, 'lib_app/reserve_view.html',{'message':'予約している書籍はありません'})
    return render(request, 'lib_app/reserve_view.html',{'reserve':reserve})

@login_required
def LendingView(request):
    lending = Lending.objects.filter(user_id__exact=request.user).exclude(returned=True)
    if lending.count() == 0:
        return render(request, 'lib_app/lending_view.html',{'message':'貸出している書籍はありません'})
    return render(request, 'lib_app/lending_view.html',{'lending':lending})

@login_required
def UserOption(request):
    return render(request, 'lib_app/user_option.html')

@login_required
def UserNameChange(request):
        user = request.user
        if request.method == 'POST':
            try:
                form = UserForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    return render(request, 'lib_app/username.html', {'form':form, 'message':'ユーザーネームを変更しました'})
            except:
                return render(request, 'lib_app/username.html', {'form':form, 'message':'エラーが発生しました'})
        else:
            form = UserForm(instance=user)
            return render(request, 'lib_app/username.html', {'form':form})

@login_required
def PasswordChange(request):
    if request.method == 'POST':
        try:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)  # セッションの更新
                    return render(request, 'lib_app/password.html', {'form':form, 'message':'パスワードを変更しました'})
        except:
            return render(request, 'lib_app/password.html', {'form':form, 'message':'エラーが発生しました'})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'lib_app/password.html', {'form':form})

def Logout(request):
    logout(request)
    return redirect(reverse('login'))

def Debug(request): #デバッグ用 完成したら消す
    help = PasswordChangeForm(user=request.user)
    return render(request, 'lib_app/debug.html', {'help':help})