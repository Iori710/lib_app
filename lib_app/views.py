from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")#ログインしていない場合ログイン画面に遷移する
def Top(request):#内容は仮
    # ユーザーモデルを取得する
    user = get_user_model()
    # ユーザーをすべて取得する
    users = user.objects.all()
    # ユーザー一覧をコンテキスト情報に入れる
    context = {'users': users}
    # top.htmlをレンダリング
    return render(request, "lib_app/top.html", context)

def Logout(request):
    logout(request)
    return redirect('/login/')