from django.contrib import admin

# Register your models here.
from .models import Category, Comment, Post,Sidebar,Favorites




admin.site.register(Sidebar)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('content','post','user')
    list_filter = ('user',)
    search_fields = ('content','post','user')
admin.site.register(Comment,CommentAdmin) 

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user','post')
    list_filter = ('user',)
    search_fields = ('user','post')
admin.site.register(Favorites,FavoritesAdmin)    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','desc')
    list_filter = ('name',)
    search_fields = ('name','desc')
admin.site.register(Category,CategoryAdmin)  

class PostAdmin(admin.ModelAdmin):
    ''' 文章详情管理 '''

    list_display = ('id', 'title','owner',  'pv',  'pub_date', )
    list_filter = ('owner',)
    search_fields = ('title', 'desc','owner','content')
    list_display_links = ('id', 'title',)
   



admin.site.register(Post, PostAdmin)


