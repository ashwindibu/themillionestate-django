# Generated by Django 3.2 on 2022-10-29 18:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_auto_20221029_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='featured_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='photo/featured_image'),
            preserve_default=False,
        ),
    ]
