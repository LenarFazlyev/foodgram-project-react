# Generated by Django 2.2.19 on 2023-09-18 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20230918_1322'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement'),
        ),
    ]
