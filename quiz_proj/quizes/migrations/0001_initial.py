# Generated by Django 3.1.2 on 2021-03-08 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('topic', models.CharField(max_length=120)),
                ('number_of_questions', models.IntegerField()),
                ('time', models.IntegerField(help_text='Duration of quiz in minutes')),
                ('required_score_to_pass', models.IntegerField(help_text='Score in percent')),
                ('difficulty', models.CharField(choices=[('Easy', 'easy'), ('Medium', 'medium'), ('Hard', 'hard')], max_length=6)),
            ],
        ),
    ]
