# Generated by Django 4.0.4 on 2022-05-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('rating', models.DecimalField(decimal_places=4, max_digits=5)),
                ('count', models.SmallIntegerField()),
            ],
        ),
    ]
