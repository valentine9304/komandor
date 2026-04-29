from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers


class GitHubLoginView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter

    @extend_schema(
        tags=["Авторизация"],
        summary="Авторизация через GitHub",
        description=(
            "Принимает access token, полученный от GitHub, и авторизует пользователя "
            "в API. В ответ возвращает токен DRF для дальнейших запросов."
        ),
        request=inline_serializer(
            name="GitHubLoginRequest",
            fields={
                "access_token": serializers.CharField(
                    help_text="Access token, полученный от GitHub OAuth."
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name="GitHubLoginResponse",
                fields={
                    "key": serializers.CharField(
                        help_text="Токен авторизации DRF."
                    ),
                },
            ),
            400: OpenApiResponse(description="Некорректный или просроченный GitHub token."),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"access_token": "gho_xxxxxxxxxxxxxxxxxxxx"},
                request_only=True,
            ),
            OpenApiExample(
                "Пример ответа",
                value={"key": "0123456789abcdef0123456789abcdef01234567"},
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
