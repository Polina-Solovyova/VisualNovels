from django.contrib import admin
from .models import Episode, Novel, UserProgress, Season, Character, Dialogue, Background, Music, Choice, UserProfile


admin.site.register(Novel)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Character)
admin.site.register(Dialogue)
admin.site.register(UserProgress)
admin.site.register(Background)
admin.site.register(Music)
admin.site.register(Choice)
admin.site.register(UserProfile)