# Generated by Django 2.1.1 on 2018-11-01 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_role_is_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(blank=True, max_length=50)),
                ('gender', models.CharField(blank=True, choices=[('', 'Не указан'), ('M', 'Мужской'), ('F', 'Женский')], max_length=1)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.EmailField(max_length=254)),
                ('cell_phone', models.CharField(blank=True, max_length=20)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('social', models.CharField(blank=True, max_length=250)),
                ('skype', models.CharField(blank=True, max_length=50)),
                ('cont_role', models.CharField(blank=True, max_length=50)),
                ('cont_surname', models.CharField(blank=True, max_length=50)),
                ('cont_name', models.CharField(blank=True, max_length=50)),
                ('cont_patronymic', models.CharField(blank=True, max_length=50)),
                ('cont_email', models.EmailField(blank=True, max_length=254)),
                ('cont_cell_phone', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]