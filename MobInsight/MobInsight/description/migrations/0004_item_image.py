# Generated by Django 4.2.5 on 2023-10-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('description', '0003_alter_item_camera'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.TextField(default='NULL'),
            preserve_default=False,
        ),
    ]