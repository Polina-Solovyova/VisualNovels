# Generated by Django 5.0.7 on 2024-07-19 21:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('poster', models.ImageField(upload_to='posters/')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='novels.novel')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='novels.season')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
                ('nickname', models.CharField(max_length=50)),
                ('avatar', models.ImageField(upload_to='avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(default=0)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='read_novels',
            field=models.ManyToManyField(through='novels.UserProgress', to='novels.series'),
        ),
    ]
