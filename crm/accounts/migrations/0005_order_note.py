# Generated by Django 3.1.2 on 2021-02-22 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210222_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
    ]