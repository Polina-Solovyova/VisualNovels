from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Novel, Episode, UserProgress, UserProfile, Dialogue
from .serializers import (
    UserProfileSerializer,
    NovelSerializer,
    EpisodeSerializer,
    UserRegisterSerializer,
    UserLoginSerializer, DialogueSerializer, NovelIdsSerializer
)
import logging

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='post',
    request_body=UserRegisterSerializer,
    operation_description="Register a new user"
)
@api_view(['POST'])
def register(request):
    data = request.data
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return Response({'errors': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'errors': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'errors': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return Response({
        'message': 'Register successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'email': user.email,
            'id': user.id,
            'username': user.username,
        }
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    operation_description="Login a user"
)
@api_view(['POST'])
def login_user(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'email': user.email,
                'id': user.id,
                'username': user.username,
            }
        }, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(
    method='post',
    operation_description="Logout a user"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


@swagger_auto_schema(
    method='get',
    operation_description="Get user profile"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user_profile = request.user.userprofile
    user_progress = UserProgress.objects.filter(user=user_profile)

    # Получаем данные профиля и прогресс
    progress_data = [
        {
            'novel': progress.current_episode.season.novel.id,
            'episode': progress.current_episode.id,
            'progress': progress.progress
        }
        for progress in user_progress
    ]

    # Создаем данные для ответа
    data = {
        'profile': {
            'avatar': user_profile.avatar.url,
            'username': user_profile.user.username,
            'diamonds': user_profile.diamonds,
        },
        'user_progress': progress_data
    }

    return Response(data)


@swagger_auto_schema(
    method='get',
    responses={200: NovelSerializer(many=True)},
    operation_description="List all novels"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def novel_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    progress_dict = {}
    for progress in UserProgress.objects.filter(user=user_profile):
        if progress.current_episode:  # Проверка, чтобы избежать ошибки
            progress_dict[progress.current_episode.id] = progress.progress

    novels = Novel.objects.all()
    data = {
        'novels': NovelSerializer(novels, many=True).data,
        'progress_dict': progress_dict
    }
    return Response(data)


@swagger_auto_schema(
    method='get',
    operation_description="Get novel progress including seasons and episodes"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def novel_progress(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    user_profile = request.user.userprofile

    # Получаем все сезоны и эпизоды
    seasons = novel.seasons.all()
    seasons_data = []

    for season in seasons:
        episodes = season.episodes.all()
        total_episodes = episodes.count()

        # Считаем количество завершённых эпизодов
        completed_episodes = UserProgress.objects.filter(
            user=user_profile,
            current_episode__in=episodes,
            progress=100.0
        ).count()

        # Находим следующий эпизод
        next_episode = episodes.filter(number=completed_episodes + 1).first()
        current_episode_id = next_episode.id if next_episode else None

        seasons_data.append({
            'season': {
                'id': season.id,
                'title': season.title,
                'number': season.number,
            },
            'episodes': {
                'current': current_episode_id,
                'completed': completed_episodes,
                'total': total_episodes
            }
        })

    return Response({'seasons': seasons_data})


@swagger_auto_schema(
    method='get',
    operation_description="Get details of a specific novel"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    first_episode = novel.seasons.first().episodes.first()
    data = {
        'title': novel.title,
        'description': novel.description,
        'cover_image': novel.cover_image.url,
        'first_episode_id': first_episode.id if first_episode else None,
    }
    return Response(data)


@swagger_auto_schema(
    method='get',
    responses={200: EpisodeSerializer(many=True)},
    operation_description="List all episodes for a specific novel"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def episode_list(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    episodes = Episode.objects.filter(season__novel=novel)
    data = {
        'episodes': EpisodeSerializer(episodes, many=True).data
    }
    return Response(data)


@swagger_auto_schema(
    method='post',
    request_body=UserProfileSerializer,
    operation_description="Upload a new avatar"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    if 'avatar' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    avatar = request.FILES['avatar']
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.avatar = avatar
    profile.save()

    return Response({'message': 'Avatar uploaded successfully', 'avatar': profile.avatar.url},
                    status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=NovelIdsSerializer,
    operation_description="Get novels"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_novels_by_ids(request):
    if request.method == 'POST':
        # Получение данных
        ids = request.data.get('ids', [])
        print(f'IDs received: {ids}')

        # Фильтрация новелл по списку ID
        novels = Novel.objects.filter(id__in=ids)
        print(f'Novels found: {novels}')

        # Преобразование новелл в сериализованный вид
        serialized_novels = NovelSerializer(novels, many=True).data
        print(f'Serialized data: {serialized_novels}')

        # Возвращаем данные в формате JSON
        return JsonResponse(serialized_novels, safe=False)
    else:
        return HttpResponseNotAllowed(['POST'])

class NovelReadingView(viewsets.ViewSet):
    @action(detail=True, methods=['get'])
    def progress(self, request, novel_id):
        try:
            novel = get_object_or_404(Novel, id=novel_id)
            user = request.user.userprofile

            # Получение прогресса пользователя
            progress = UserProgress.objects.filter(user=user, novel=novel).first()

            # Получение общего количества эпизодов
            total_episodes = Episode.objects.filter(season__novel=novel).count()

            if not progress:
                return Response({
                    "completed_episodes": 0,
                    "total_episodes": total_episodes,
                    "progress": 0,
                    "status": "New",
                    "current_episode": None
                }, status=status.HTTP_200_OK)

            current_episode_id = progress.current_episode.id if progress.current_episode else None

            # Подсчёт завершённых эпизодов
            completed_episodes = Episode.objects.filter(
                season__novel=novel,
                id__lte=current_episode_id
            ).count()

            # Проверяем, завершена ли новелла (если пользователь завершил последний диалог последнего эпизода)
            is_completed = completed_episodes >= total_episodes
            progress_percent = 100 if is_completed else (completed_episodes / total_episodes * 100)
            status_text = "Completed" if is_completed else "In Progress"

            return Response({
                "completed_episodes": completed_episodes,
                "total_episodes": total_episodes,
                "progress": progress_percent,
                "status": status_text,
                "current_episode": current_episode_id
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_current_dialogue(self, request, novel_id):
        novel = get_object_or_404(Novel, id=novel_id)
        user = request.user

        # Получаем профиль пользователя
        user_profile = get_object_or_404(UserProfile, user=user)

        # Получаем или создаем прогресс пользователя по данной новелле
        progress, created = UserProgress.objects.get_or_create(user=user_profile, novel=novel)

        # Если прогресс создан заново или не содержит текущий диалог, начинаем с первого диалога
        if created or not progress.current_dialogue:
            first_episode = novel.seasons.first().episodes.first()
            first_dialogue = first_episode.dialogues.first() if first_episode else None

            if first_episode and first_dialogue:
                progress.current_episode = first_episode
                progress.current_dialogue = first_dialogue
                progress.save()
            else:
                return Response({"detail": "No episodes or dialogues found for this novel."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Сериализуем текущий диалог и возвращаем его
        serializer = DialogueSerializer(progress.current_dialogue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, novel_id):
        try:
            novel = get_object_or_404(Novel, id=novel_id)
            user = request.user.userprofile
            progress = get_object_or_404(UserProgress, user=user, novel=novel)
            episode_completed = False

            if 'save_progress' in request.data:
                # Ищем следующий диалог в текущем эпизоде
                next_dialogue = Dialogue.objects.filter(
                    episode=progress.current_episode,
                    id__gt=progress.current_dialogue.id
                ).first()

                if next_dialogue:
                    progress.current_dialogue = next_dialogue
                else:
                    next_episode = Episode.objects.filter(
                        season__novel=novel,
                        id__gt=progress.current_episode.id
                    ).first()
                    episode_completed = True

                    if next_episode:
                        next_dialogue = next_episode.dialogues.first()
                        progress.current_episode = next_episode
                        progress.current_dialogue = next_dialogue
                    else:
                        # Если больше эпизодов нет, возвращаем флаг завершения эпизода
                        episode_completed = True

                progress.save()
                serializer = DialogueSerializer(next_dialogue)
                return Response({
                    "dialogue": serializer.data,
                    "episode_completed": episode_completed
                }, status=status.HTTP_200_OK)

            else:
                # Возвращаем текущий диалог без обновления прогресса
                serializer = DialogueSerializer(progress.current_dialogue)
                return Response({
                    "dialogue": serializer.data,
                    "episode_completed": episode_completed
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

