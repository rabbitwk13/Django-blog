# Generated by Django 4.2.5 on 2023-11-06 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_favorites'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorites',
            options={'verbose_name': '收藏管理', 'verbose_name_plural': '收藏管理'},
        ),
    ]