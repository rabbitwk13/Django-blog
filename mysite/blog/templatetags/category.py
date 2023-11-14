#自定义模板标签
from django import template
from blog.models import Category, Sidebar, Post

register = template.Library()

@register.simple_tag
def get_category_list():
    # 全站的分类
    return Category.objects.all()
@register.simple_tag
def get_sidebar_list():
    # 侧边栏
    return Sidebar.get_sidebar()
@register.simple_tag
def get_new_post():
    return Post.objects.all().order_by('-pub_date')[:6]

@register.simple_tag
def get_hot_post():
    return Post.objects.all().filter()[:6]

@register.simple_tag
def get_hot_pv_post():
    # 手动热门推荐
    return Post.objects.order_by('-pv')[:6]

@register.simple_tag
def get_archives():
    # 文章归档
    return Post.objects.dates('add_date', 'month', order='DESC')[:6] #desc降序


