# Generated by Django 3.2 on 2021-05-11 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_likeanswer_opinion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answersAmount',
        ),
    ]
