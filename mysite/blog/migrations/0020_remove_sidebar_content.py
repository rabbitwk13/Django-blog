# Generated by Django 4.2.5 on 2023-11-04 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_remove_post_is_hot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sidebar',
            name='content',
        ),
    ]