# Generated by Django 5.0.7 on 2024-07-20 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0010_rename_episode_userprogress_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
