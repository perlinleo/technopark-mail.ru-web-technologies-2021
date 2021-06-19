# Generated by Django 3.2 on 2021-04-21 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='authorID',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='likeanswer',
            old_name='answerID',
            new_name='answer',
        ),
        migrations.RenameField(
            model_name='likeanswer',
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='likequestion',
            old_name='questionID',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='likequestion',
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='authorID',
            new_name='author',
        ),
    ]
