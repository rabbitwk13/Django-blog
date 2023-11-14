from dataclasses import field
from tkinter.ttk import Style
from django import forms
from .models import Post
from .models import Category, Post,Comment
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # 可以上传文件的富文本框

class PostForm(forms.ModelForm):
    title = forms.CharField(label="文章标题",max_length=61, widget=forms.TextInput(attrs={"class": "content is-medium","size": 88,'placeholder':'输入文章标题'}))
    desc = forms.CharField(label='文章描述',max_length=200, widget=forms.Textarea(attrs={"class": "textarea is-medium","id":'id_desc','placeholder':'输入文章描述'}))
    content = RichTextUploadingFormField(label='文章内容',widget=CKEditorUploadingWidget())
    owner = forms.CharField(label="作者",max_length=61, widget=forms.TextInput(attrs={"class": "content is-medium",'placeholder':'输入文章的作者' ,"size": 11}))
    category = forms.ModelChoiceField(label='文章分类选项',queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'desc', 'content','owner','category']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label="添加文章分类",max_length=61, widget=forms.TextInput(attrs={"class": "content is-medium",'placeholder':'输入文章分类'}))
    class Meta:
        model = Category
        fields = ['name']


