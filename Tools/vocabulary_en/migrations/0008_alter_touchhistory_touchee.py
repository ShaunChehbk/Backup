# Generated by Django 4.0.4 on 2022-05-27 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary_en', '0007_touchhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touchhistory',
            name='touchee',
            field=models.ForeignKey(db_constraint=False, default=0, on_delete=django.db.models.deletion.CASCADE, to='vocabulary_en.word'),
        ),
    ]
