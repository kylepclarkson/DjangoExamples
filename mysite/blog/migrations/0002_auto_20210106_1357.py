# Generated by Django 3.1.2 on 2021-01-06 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='created_on_date',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]