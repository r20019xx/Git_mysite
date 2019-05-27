import random
import time
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from login.models import Users

def index(request):
  if request.method == 'GET':
    # 認證已登入cookie，若無則顯示登入註冊頁面
    ticket = request.COOKIES.get('ticket')
    if not ticket:
      return render(request, 'index.html')
    # 有則導向已登入後應顯示畫面
    if Users.objects.filter(u_ticket=ticket).exists():
      return HttpResponseRedirect('/suc/')
    else:
      return render(request, 'index.html')

def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    if request.method == 'POST':
        # 註冊
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 判斷使用者不在資料庫中避免重複註冊
        if Users.objects.filter(u_name=name).exists() != True:
            # 確認帳密非空
            if name !='' and password !='':
                # 對密碼進行加密
                password = make_password(password)
                Users.objects.create(u_name=name, u_password=password)
                return HttpResponseRedirect('/login/')
            else:
                messages.success(request, '帳戶名稱或密碼不可為空')
                return HttpResponseRedirect('/regist/')
        else:
            messages.success(request, '此用戶名已註冊，跳轉回登入頁面')
            return HttpResponseRedirect('/login/')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 如果登入成功，繫結引數到cookie中，set_cookie
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 查詢使用者是否在資料庫中
        if Users.objects.filter(u_name=name).exists():
            user = Users.objects.get(u_name=name)
            if check_password(password, user.u_password):
                # ticket = 'agdoajbfjad'
                ticket = ''
                for i in range(15):
                    s = 'abcdefghijklmnopqrstuvwxyz'
                    # 獲取隨機的字串
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)
                # 繫結令牌到cookie裡面
                # response = HttpResponse()
                response = HttpResponseRedirect('/suc/')
                # max_age 存活時間(秒)
                response.set_cookie('ticket', ticket, max_age=10000)
                # 存在服務端
                user.u_ticket = ticket
                user.save()  # 儲存
                messages.success(request, '註冊成功，跳轉回登入頁面')
                return response
            else:
                # return HttpResponse('使用者密碼錯誤')
                messages.success(request, '使用者密碼錯誤')
                return HttpResponseRedirect('/login/')
        else:
            # return HttpResponse('使用者不存在')
            messages.success(request, '使用者不存在，跳轉到註冊頁面')
            return HttpResponseRedirect('/regist/')

def logout(request):
  if request.method == 'GET':
    # response = HttpResponse()
    response = HttpResponseRedirect('/')
    response.delete_cookie('ticket')
    messages.success(request, '已成功登出')
    return response

def suc(request):
  return render(request, 'suc.html')