from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список постов",
        description=(
            "Возвращает список всех постов. "
            "Доступно без авторизации. Фильтрация по автору "
            "и дате создания, а также сортировка."
        ),
    ),
    retrieve=extend_schema(
        summary="Детальная информация о посте",
        description="Возвращает один пост по его ID. Доступно без авторизации.",
    ),
    create=extend_schema(
        summary="Создание поста",
        description=(
            "Создает новый пост. Доступно только авторизованным пользователям. "
        ),
    ),
    update=extend_schema(
        summary="Полное обновление поста",
        description="Полностью обновляет пост. Доступно только автору поста.",
    ),
    partial_update=extend_schema(
        summary="Частичное обновление поста",
        description="Частично обновляет пост. Доступно только автору поста.",
    ),
    destroy=extend_schema(
        summary="Удаление поста",
        description="Удаляет пост. Доступно только автору поста.",
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filterset_fields = ("author", "created_at")
    ordering_fields = ("created_at", "likes_count", "title")
    ordering = ("-created_at",)

    def get_queryset(self):
        return Post.objects.select_related("author").annotate(
            likes_count=Count("likes")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)