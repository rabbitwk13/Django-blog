from ast import keyword
from multiprocessing import context
from unicodedata import category
from webbrowser import get
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category,Post,Comment,Favorites
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.core.cache import cache
#新添功能
from django.shortcuts import render, redirect
from .forms import PostForm, CategoryForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import Post, Sidebar 


# Create your views here.
def index(request):
    category_list=Category.objects.all() #查询所有分类
    post_list=Post.objects.all()         #查询所有文章
     # 分页方法
    paginator = Paginator(post_list, 6)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request,'blog/index.html',context)

def category_list(request,category_id):
    category=get_object_or_404(Category,id=category_id)
    #获取当前分类所属文章
    posts = category.post_set.all()
    # 分页方法
    paginator = Paginator(posts, 6)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context={'category':category,'page_obj': page_obj}
    return render(request,'blog/list.html',context)

def post_detail(request,post_id):
    if request.user.is_authenticated:
        post=get_object_or_404(Post,id=post_id)
        #文章详情页
        #查询上下篇
        prev_post=Post.objects.filter(id__lt=post_id).last() #上一篇
        next_post=Post.objects.filter(id__gt=post_id).first() #下一篇
        # 使用缓存获取浏览量
        pv_key = f'post_{post_id}_pv'
        pv = cache.get(pv_key)

        if pv is None:
        # 如果缓存中没有浏览量，则从数据库中获取并存入缓存
            pv = Post.objects.filter(id=post_id).update(pv=F('pv') + 1)
            cache.set(pv_key, pv + 1, 3600) # 将浏览量存入缓存，设置过期时间为1小时
        else:
        # 如果缓存中有浏览量，则直接更新浏览量
            Post.objects.filter(id=post_id).update(pv=F('pv') + 1)
            cache.set(pv_key, pv + 1, 3600) # 将更新后的浏览量存入缓存，设置过期时间为1小时
        # 使用缓存更新浏览量
        comments = Comment.objects.filter(post=post)
        is_favorite = Favorites.objects.filter(user=request.user, post=post, is_favorite=True).exists()
            
        context = {
            'post': post,
            'prev_post': prev_post,
            'next_post': next_post,
            'comments': comments,
            'is_favorited': is_favorite,
        }
        
        
        return render(request, 'blog/detail.html', context)
    else:
        post=get_object_or_404(Post,id=post_id)
        #文章详情页
        #查询上下篇
        prev_post=Post.objects.filter(id__lt=post_id).last() #上一篇
        next_post=Post.objects.filter(id__gt=post_id).first() #下一篇
        # 使用缓存获取浏览量
        pv_key = f'post_{post_id}_pv'
        pv = cache.get(pv_key)

        if pv is None:
        # 如果缓存中没有浏览量，则从数据库中获取并存入缓存
            pv = Post.objects.filter(id=post_id).update(pv=F('pv') + 1)
            cache.set(pv_key, pv + 1, 3600) # 将浏览量存入缓存，设置过期时间为1小时
        else:
        # 如果缓存中有浏览量，则直接更新浏览量
            Post.objects.filter(id=post_id).update(pv=F('pv') + 1)
            cache.set(pv_key, pv + 1, 3600) # 将更新后的浏览量存入缓存，设置过期时间为1小时
        # 使用缓存更新浏览量
        comments = Comment.objects.filter(post=post)
        context = {
            'post': post,
            'prev_post': prev_post,
            'next_post': next_post,
            'comments': comments,
            
        }
        
        
        return render(request, 'blog/detail.html', context)
def search(request):
    keyword=request.GET.get('keyword')
    if not keyword:
        post_list=Post.objects.all()
    else:
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword)| Q(owner__icontains=keyword))
     # 分页方法
    paginator = Paginator(post_list, 6)  # 第二个参数代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
   
    context={
       'page_obj': page_obj
    }
    return render(request,'blog/index.html',context)

def archives(request,year,month):
    post_list=Post.objects.filter(add_date__year=year,add_date__month=month)
      # 分页方法
    paginator = Paginator(post_list, 6)  # 第二个参数代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context={'page_obj': page_obj,'year':year,'month':month}
    return render(request,'blog/archives_list.html',context)

def add_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid() :
         
           # ... 保存表单
            post = post_form.save(commit=False) 
            post.save()
            # 重定向等后续操作
            return redirect('blog:index')
    else:
        post_form = PostForm()  # 创建空表单实例
    context = {
        'post_form': post_form,
        }
    return render(request, 'blog/add_post.html', context)

@login_required
def comment(request):
    if request.method == 'POST':
        # 获取数据
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        
        # 保存到数据库
        post = Post.objects.get(id=post_id)
        comment = Comment(content=content, post=post,user=request.user)
        comment.save()
        
        # 重定向到详情页
        return redirect('blog:post_detail', post_id=post_id)

def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid() :
           # ... 保存表单
            category = category_form.save(commit=False) 
            category.save()
            # 重定向等后续操作
            return redirect('blog:index')
    else:
        category_form = CategoryForm()
    context = {
        'category_form': category_form,
        }
    return render(request, 'blog/add_category.html', context)


@login_required
def favorite_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    favorites = Favorites.objects.filter(user=user, post=post)
    
    if favorites:
        # 取消收藏文章
        favorites.delete()
    else:
        # 添加文章到收藏夹中
        Favorites.objects.create(user=user, post=post,is_favorite=True)
    return redirect('blog:post_detail', post_id=post_id)
