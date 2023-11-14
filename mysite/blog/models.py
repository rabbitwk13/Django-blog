from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property  # 缓存装饰器
from django.template.loader import render_to_string  # 渲染模板
from django.utils import timezone
from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=32,verbose_name="分类名称")
    desc=models.TextField(max_length=200,blank=True,default='',verbose_name='分类描述')
    add_date=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    pub_date=models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        verbose_name='博客分类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name


    
class Post(models.Model):
    title=models.CharField(max_length=61,verbose_name='文章标题')
    desc=models.TextField(max_length=200,blank=True,default='',verbose_name='文章描述')
    content= RichTextUploadingField(verbose_name='文章内容')
    owner=models.CharField(max_length=61,verbose_name='作者')
    pv=models.IntegerField(default=0,verbose_name='浏览量')
    add_date=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    pub_date=models.DateTimeField(auto_now=True,verbose_name='修改时间')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='文章分类')
    class Meta:
        verbose_name='文章'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='评论文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='评论用户')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    class Meta:
        verbose_name='评论'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.content

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name="收藏文章")
    is_favorite=models.BooleanField(default=False,verbose_name='是否收藏')
    class Meta:
        verbose_name='收藏管理'
        verbose_name_plural=verbose_name

    def __str__(self):
        return f'{self.user.username}的收藏文章管理'
    
class Sidebar(models.Model):
    STATUS = (
        (1, '隐藏'),
        (2, '展示')
    )

    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '更新文章'),
        (3, '热门文章'),
        (4, '评论'),
        (5, '文章归档'),
        (6, 'HTML')
    )
    title = models.CharField(max_length=50, verbose_name="模块名称")  #  模块名称
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name="展示类型")   # 隐藏  显示状态
    sort = models.PositiveIntegerField(default=1,  verbose_name="排序", help_text='序号越小越靠前')
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="状态")        
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 时间
    

    class Meta:
        verbose_name = "侧边栏项目管理"
        verbose_name_plural = verbose_name
        ordering = ['sort']
    def __str__(self):
        return self.title
    
    @classmethod    # 类方法装饰器，这个就变成了这个类的一个方法可以调用
    def get_sidebar(cls):
        return cls.objects.filter(status=2)   # 查询到所有允许展示的模块
    @property  
    def get_content(self):
        if self.display_type == 1:
            context = {

            }
            return render_to_string('blog/sidebar/search.html', context=context)
        elif self.display_type == 2:
            context = {
                
            }
            return render_to_string('blog/sidebar/new_post.html', context=context)
        elif self.display_type == 3:
            context = {

            }
            return render_to_string('blog/sidebar/hot_post.html', context=context)
        elif self.display_type == 4:  
            context = {

            }  
            return render_to_string('blog/sidebar/commment.html', context=context) 
        elif self.display_type == 5:   # 文章归档
            context = {

            }
            return render_to_string('blog/sidebar/archives.html', context=context)
        elif self.display_type == 6:   # 自定义侧边栏
           
            context = {

            }
            return render_to_string('blog/sidebar/music.html', context=context)

   
