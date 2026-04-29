import django_filters

from posts.models import Post


class PostFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Post
        fields = ("author", "created_after", "created_before")