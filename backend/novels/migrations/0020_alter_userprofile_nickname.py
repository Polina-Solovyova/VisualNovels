# Generated by Django 5.0.7 on 2024-07-22 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0019_alter_userprogress_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(max_length=100),
        ),
    ]
