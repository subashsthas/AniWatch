# Generated by Django 3.1.7 on 2021-05-01 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210501_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watched',
            name='animeMovie',
        ),
        migrations.RemoveField(
            model_name='watched',
            name='animeSeries',
        ),
        migrations.AddField(
            model_name='watched',
            name='anime',
            field=models.ManyToManyField(to='main.Movies'),
        ),
    ]
