# Generated by Django 2.2.19 on 2023-09-09 16:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230909_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='cookingtime',
            new_name='cooking_time',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='title',
        ),
        migrations.AddField(
            model_name='recipe',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, verbose_name='Название блюда'),
            preserve_default=False,
        ),
    ]
