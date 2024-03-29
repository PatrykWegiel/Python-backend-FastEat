# Generated by Django 4.0.3 on 2022-06-07 21:28

from django.db import migrations
import django_resized.forms
import menu.models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuaddon',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=-1, size=[150, 150], upload_to=menu.models.menu_addon_image_upload),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=-1, size=[150, 150], upload_to=menu.models.menu_item_image_upload),
        ),
    ]
