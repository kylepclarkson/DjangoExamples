# Generated by Django 3.1.2 on 2021-01-08 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210107_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='last_modified',
            field=models.DateField(auto_now_add=True),
        ),
    ]