# Generated by Django 4.0.4 on 2022-04-26 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark_collection', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bookmark',
            new_name='Entry',
        ),
    ]
