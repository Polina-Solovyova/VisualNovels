# Generated by Django 5.0.7 on 2024-08-12 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0029_alter_userprogress_current_dialogue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprogress',
            name='current_dialogue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_progress_dialogues', to='novels.dialogue'),
        ),
        migrations.AlterField(
            model_name='userprogress',
            name='current_episode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novels.episode'),
        ),
    ]
