# Generated by Django 3.1.7 on 2021-05-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210501_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watched',
            name='anime',
            field=models.ManyToManyField(to='main.Movies'),
        ),
    ]
