# Generated by Django 3.2.16 on 2023-09-27 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20230926_0831'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username', 'email'), 'verbose_name': 'пользователя', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
