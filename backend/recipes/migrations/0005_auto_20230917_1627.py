# Generated by Django 2.2.19 on 2023-09-17 13:27

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230917_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFFFF', image_field=None, max_length=25, samples=None),
        ),
    ]