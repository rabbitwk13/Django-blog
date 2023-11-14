from django.urls import path
from . import views

app_name = 'users'   # 定义一个命名空间，用来区分不同应用之间的链接地址

urlpatterns = [ 
    path('login/', views.login_view, name='login'),
    # 编辑用户信息 
    path('register/', views.register, name='register'),
    # 注册
   
    path('user_profile/',views.user_profile,name='user_profile'),
    path('logout/',views.logout_view,name='logout'),
    path('editor_users/',views.editor_users,name='editor_users'),
    path('register_cue/', views.register_cue, name='register_cue'),
   
]