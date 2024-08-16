from django.urls import path
from . import views
from .views import NovelReadingView

urlpatterns = [
    # User authentication and registration
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # User dashboard
    path('profile/', views.profile_view, name='profile'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),

    # Novel related paths
    path('', views.novel_list, name='novel_list'),
    path('novels/', views.get_novels_by_ids, name='novel_detail'),
    path('novel/<int:novel_id>/current-dialogue/', NovelReadingView.as_view({'get': 'get_current_dialogue'})),
    path('novel/<int:novel_id>/update-progress/', NovelReadingView.as_view({'post': 'update_progress'})),
    path('novel/<int:novel_id>/progress/', NovelReadingView.as_view({'get': 'progress'})),
]
