# Generated by Django 3.2 on 2021-04-22 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_tag_popularity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likequestion',
            options={'verbose_name': 'Question reacts', 'verbose_name_plural': 'Question reacts'},
        ),
    ]
