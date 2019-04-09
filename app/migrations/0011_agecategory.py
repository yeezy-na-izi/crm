# Generated by Django 2.1.2 on 2018-11-07 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start', models.PositiveSmallIntegerField(null=True)),
                ('end', models.PositiveSmallIntegerField(null=True)),
            ],
        ),
    ]