# Generated by Django 3.2 on 2021-05-04 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210504_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likeanswer',
            name='opinion',
            field=models.BooleanField(default=True, verbose_name='Like?'),
        ),
    ]
