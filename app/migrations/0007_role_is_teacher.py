# Generated by Django 2.1.1 on 2018-10-30 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20181029_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]