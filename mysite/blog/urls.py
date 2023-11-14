from django.urls import URLPattern, path
from . import views

app_name = "blog"  # 定义一个命名空间，用来区分不同应用之间的链接地址

urlpatterns = [
    path('',views.index,name='index'),
    path('category/<int:category_id>/',views.category_list,name='category_list'),
    path('post/<int:post_id>/',views.post_detail,name='post_detail'),
    path('search/',views.search,name='search'),
    path('archives/<int:year>/<int:month>/',views.archives,name='archives'),
    path('add_post/', views.add_post, name='add_post'),
    path('comment/', views.comment, name='comment'),
    path('add_category/', views.add_category, name='add_category'),
    path('post/<int:post_id>/favorite/', views.favorite_post, name='favorite'),
]
