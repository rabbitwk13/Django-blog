# Generated by Django 4.2.5 on 2023-11-06 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_favorites_is_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorites',
            name='is_favorite',
        ),
    ]
