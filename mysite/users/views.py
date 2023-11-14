import email
from genericpath import exists
from multiprocessing import context
from typing import Any
from urllib import request
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q
from tarfile import NUL
from django.http.request import HttpRequest
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import is_valid_path
from .forms import LoginForm,RegisterForm,UserForm,UserProfileForm
from .models import UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.
class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        # 尝试从数据库中获取与给定用户名匹配的用户对象
        try:
            user = User.objects.get(Q(username=username))
            # 如果用户存在且密码正确，则返回该用户对象
            if user.check_password(password):
                return user
        except Exception:
            # 如果发生异常（例如用户不存在），则返回None
            return None

def login_view(request):
    if request.method != 'POST':
        form = LoginForm()  # 如果请求方法不是POST，则创建一个空的登录表单
    else:
        form = LoginForm(request.POST)  # 如果请求方法是POST，则使用提交的数据创建表单实例
        if form.is_valid():  # 验证表单数据是否有效
            username = form.cleaned_data['username']  # 获取用户名字段的值
            password = form.cleaned_data['password']  # 获取密码字段的值
            user = authenticate(request, username=username, password=password)  # 使用Django内置的authenticate函数进行身份验证
            if user is not None:  # 如果身份验证成功
                login(request, user)  # 使用Django内置的login函数将用户登录到系统中
                return redirect('users:user_profile')  # 重定向到用户的个人资料页面
            else:
                return redirect('users:register_cue')  # 如果身份验证失败，则重定向到注册页面或错误提示页面
    context = {'form': form}  # 将表单实例添加到上下文中，以便在模板中使用
    return render(request, 'users/login.html', context)  # 渲染登录页面并返回响应

def register(request):
    # 检查请求方法是否为POST
    if request.method != "POST":
        # 如果请求方法不是POST，则创建一个空的注册表单对象
        form = RegisterForm()
    else:
        # 如果请求方法是POST，则使用提交的数据创建表单对象
        form = RegisterForm(request.POST)
        # 验证表单数据是否有效
        if form.is_valid():
            # 保存表单数据但不立即提交到数据库
            new_user = form.save(commit=False)
            # 设置新用户的密码
            new_user.set_password(form.cleaned_data.get('password'))
            # 设置新用户的用户名
            new_user.username = form.cleaned_data.get('username')
            # 将新用户保存到数据库
            new_user.save()
            # 重定向到注册成功的页面
            return redirect('users:register_cue')
    # 将表单对象传递给模板上下文
    context = {'form': form}
    # 渲染注册页面并返回响应
    return render(request, 'users/register.html', context)

                                                           
def register_cue(request):
  return render(request, 'users/register_cue.html') #返回注册响应界面
       


@login_required(login_url='users:login') #这是一个装饰器，它的作用是确保只有登录的用户才能访问这个视图函数。如果未登录的用户尝试访问这个视图函数，他们将被重定向到指定的登录页面
def user_profile(request):
      user = User.objects.get(username=request.user) #从数据库中获取与当前登录用户匹配的用户对象
      return render(request,'users/user_profile.html',{'user':user}) #获取当前登录用户的个人资料信息，并将其渲染到用户的个人资料页面上

def logout_view(request):
      logout(request)
      return redirect('users:login') #返回退出登录界面

@login_required(login_url='users:login')
def editor_users(request):
    """ 编辑用户信息 """
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            # 如果表单有效，保存用户信息和用户配置文件
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:
            # 如果用户配置文件不存在，创建一个新的用户配置文件
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            # 如果用户配置文件不存在，创建一个新的用户配置文件
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()
    # 渲染模板并传递局部变量
    return render(request, 'users/editor_users.html', locals())