# Generated by Django 5.0.7 on 2024-07-20 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0011_userprogress_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprogress',
            name='progress',
        ),
    ]
