from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
class LoginForm(forms.Form):  # 定义一个名为LoginForm的登录表单类
    username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={'placeholder': '请输入用户名', 'class': 'inputItem'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'placeholder': '请输入密码', 'class': 'inputItem'}))
     #指定了该字段的渲染方式为文本/密码输入框，并设置了额外的属性：
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password') #从已清理的数据字典中获取相应字段的值。
        if username == password:
            raise forms.ValidationError('用户名与密码不可相同') #如果用户名和密码相同，则抛出一个验证错误，错误信息为"用户名与密码不可相同"。
        return password
class RegisterForm(forms.ModelForm): #定义一个名为RegisterForm的注册表单类
        username = forms.CharField(label='用户名',min_length=1,widget=forms.TextInput(attrs={'placeholder': '请输入用户名','class':'inputItem'}))
        password=forms.CharField(label='密码',min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '请输入密码','class':'inputItem'}))
        password1=forms.CharField(label='再次输入密码',min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '请再次输入密码','class':'inputItem'}))
        #定义三个表单字段：`username`、`password` 和 `password1`。这些字段对应于用户注册的 `username`、`password` 和确认密码。每个字段都有特定的属性，如标签、最小长度和用于样式化的小部件属性。
        class Meta:
             model = User
             fields=('username','password') #为表单指定元数据。`Meta` 类用于提供有关表单的附加信息，例如关联的模型（`User`）和包含在表单中的字段（`'username'` 和 `'password'`）。
        def clean_username(self):
             username=self.cleaned_data.get('username')
             exists=User.objects.filter(username=username).exists() 
             if exists:
                  raise forms.ValidationError("用户名已经存在")
             return username #定义一个名为 `clean_username` 的方法，用于对 `username` 字段进行自定义验证。它检查提供的用户名是否已经存在于数据库中（`User.objects.filter(username=username).exists()`），如果存在，则引发验证错误。
        def clean_password1(self):
             if self.cleaned_data['password'] != self.cleaned_data['password1']: # 验证密码
                  raise forms.ValidationError("两次输入密码不一致")
             return self.cleaned_data['password1'] #定义一个名为 `clean_password1` 的方法，用于对 `password1` 字段进行自定义验证。它检查密码及其确认是否匹配，如果不匹配，则引发验证错误。
        

class UserForm(forms.ModelForm):
     username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input'
    }))

     class Meta:
          model=User
          fields=('username',)
#定义了一个名为 `username` 的表单字段，该字段对应于 `User` 模型中的 `username` 字段。通过使用 `forms.CharField`，指定了这是一个字符型字段。`widget=forms.TextInput(attrs={'class': 'input'})` 部分定义了该字段在HTML中的呈现方式，包括使用 `TextInput` 小部件和添加了一个CSS类（`'input'`）。
class UserProfileForm(forms.ModelForm):
     class Meta:
          model=UserProfile
          fields=('nike_name','desc','gexing','birthday','gender','address','image')
#通过 `Meta` 类定义了一些元数据，指明了这个表单与哪个模型关联以及包含哪些字段。在这里，关联的模型是 `UserProfile`，并且包含了该模型中的一些字段，包括：
# - `nike_name`: 用户昵称
# - `desc`: 用户描述
# - `gexing`: 用户个性
# - `birthday`: 用户生日
# - `gender`: 用户性别
# - `address`: 用户地址
# - `image`: 用户图像

# 这些字段定义了在用户界面上收集用户个人资料信息的表单。通过在 `Meta` 类中指定这些字段，Django 将根据 `UserProfile` 模型自动生成表单元素，并且在验证和保存表单数据时与模型进行适当的映射。