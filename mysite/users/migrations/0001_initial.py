# Generated by Django 4.2.5 on 2023-09-15 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nike_name', models.CharField(blank=True, default='', max_length=23, verbose_name='昵称')),
                ('desc', models.TextField(blank=True, default='', max_length=200, verbose_name='个人简介')),
                ('gexing', models.CharField(blank=True, default='', max_length=100, verbose_name='个性签名')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=6, verbose_name='性别')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='地址')),
                ('image', models.ImageField(default='images/default.png', upload_to='images/%Y/%m', verbose_name='用户头像')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
    ]
