# Generated by Django 3.1.14 on 2023-09-28 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20230927_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.TextField(max_length=40),
        ),
        migrations.AlterField(
            model_name='post',
            name='booktitle',
            field=models.TextField(max_length=80),
        ),
        migrations.AlterField(
            model_name='post',
            name='main',
            field=models.TextField(max_length=150),
        ),
        migrations.AlterField(
            model_name='post',
            name='sub',
            field=models.TextField(max_length=800),
        ),
    ]