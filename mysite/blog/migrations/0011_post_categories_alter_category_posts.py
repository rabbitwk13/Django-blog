# Generated by Django 4.2.5 on 2023-10-30 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_category_posts_tag_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='category_posts', to='blog.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='posts',
            field=models.ManyToManyField(related_name='post_categories', to='blog.post'),
        ),
    ]