# Generated by Django 5.0.7 on 2024-07-19 22:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0002_remove_userprofile_balance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='poster',
        ),
        migrations.AddField(
            model_name='novel',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/novels/covers/'),
        ),
        migrations.AddField(
            model_name='novel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='season',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='season',
            name='description',
            field=models.TextField(default='novel'),
        ),
        migrations.AddField(
            model_name='season',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='novel',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='season',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='static/default_avatar.png', upload_to='avatars/'),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('number', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/novels/background/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='novels/audio/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='novels.season')),
            ],
        ),
        migrations.AlterField(
            model_name='userprogress',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.episode'),
        ),
        migrations.DeleteModel(
            name='Series',
        ),
    ]
