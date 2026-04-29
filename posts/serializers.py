from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "likes_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author", "likes_count", "created_at", "updated_at")