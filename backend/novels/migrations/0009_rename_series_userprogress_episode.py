# Generated by Django 5.0.7 on 2024-07-20 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0008_remove_userprogress_progress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprogress',
            old_name='series',
            new_name='episode',
        ),
    ]
