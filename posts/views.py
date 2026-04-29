from django.db.models import Count
from rest_framework import permissions, viewsets

from posts.models import Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer


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