from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    diamonds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Novel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='novels/covers/')

    def __str__(self):
        return self.title


class Character(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='novels/characters/')

    def __str__(self):
        return self.name


class Background(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='novels/backgrounds/')

    def __str__(self):
        return self.title


class Music(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='novels/music/')

    def __str__(self):
        return self.title


class Season(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='seasons')
    title = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=0)
    description = models.TextField(default='novel')

    def __str__(self):
        return f"{self.novel.title} - Season {self.number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    number = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('read_episode', args=[self.season.novel.id, self.id])

    def __str__(self):
        return f"{self.id}"


class Dialogue(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='dialogues')
    text = models.TextField()
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    background = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True, blank=True)
    music = models.ForeignKey(Music, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=10, choices=(('left', 'Left'), ('right', 'Right'), ('center', 'Center')),
                                default='center')
    choices = models.ManyToManyField('Choice', blank=True)


    def __str__(self):
        return f"{self.episode} - {self.character}: {self.text[:20]}"


class Choice(models.Model):
    text = models.CharField(max_length=255)
    next_dialogue = models.ForeignKey(Dialogue, related_name='previous_choices', on_delete=models.SET_NULL, null=True)


class UserProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, null=True)
    current_episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True)
    current_dialogue = models.ForeignKey(Dialogue, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='user_progress_dialogues')
    progress = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'current_episode', 'current_dialogue'], name='unique_user_progress')
        ]

    def __str__(self):
        return f"{self.user} - {self.current_episode} - {self.progress}%"
