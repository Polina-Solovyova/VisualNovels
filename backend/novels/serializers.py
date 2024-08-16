from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Novel, Episode, UserProgress, Dialogue, Choice


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'diamonds']


class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = ['id', 'title', 'description', 'cover_image']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'number']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['current_episode', 'current_dialogue']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class DialogueSerializer(serializers.ModelSerializer):
    character_name = serializers.CharField(source='character.name', read_only=True)
    character_image = serializers.ImageField(source='character.image', read_only=True)
    background = serializers.ImageField(source='background.image', read_only=True)

    class Meta:
        model = Dialogue
        fields = ['id', 'text', 'character_name', 'character_image', 'background', 'music', 'position', 'choices']


class NovelIdsSerializer(serializers.ModelSerializer):
    ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Novel.objects.all())

    class Meta:
        model = Novel
        fields = ['ids']
