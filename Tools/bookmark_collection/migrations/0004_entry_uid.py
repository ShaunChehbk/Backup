# Generated by Django 4.0.4 on 2022-05-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark_collection', '0003_alter_entry_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='uid',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
