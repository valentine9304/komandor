from django.urls import path

from accounts.views import GitHubLoginView

urlpatterns = [
    path("github/", GitHubLoginView.as_view(), name="github-login"),
]