# Generated by Django 4.2.5 on 2023-10-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AlterField(
            model_name='post',
            name='owner',
            field=models.CharField(max_length=61, verbose_name='作者'),
        ),
    ]
