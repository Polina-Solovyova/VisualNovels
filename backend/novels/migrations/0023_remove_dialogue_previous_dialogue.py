# Generated by Django 5.0.7 on 2024-08-12 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0022_alter_choice_options_remove_character_side_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dialogue',
            name='previous_dialogue',
        ),
    ]
