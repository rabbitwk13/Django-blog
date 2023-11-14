from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

# Register your models here.
from django.contrib.auth.admin import UserAdmin

# 注册模型到 Django 管理界面

# 首先，注销默认的 User 模型，因为我们要使用自定义的 UserProfileAdmin
admin.site.unregister(User)

# 创建一个内联模型，用于在用户管理页面显示 UserProfile 的信息
class UserProfileInline(admin.StackedInline):
    model = UserProfile

# 创建一个自定义的 UserAdmin，将 UserProfileInline 内联到 UserAdmin 中
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

# 将自定义的 UserProfileAdmin 注册到 Django 的管理界面，用于管理 User 模型
admin.site.register(User, UserProfileAdmin)