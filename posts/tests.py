from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Like, Post

User = get_user_model()


class PostAPITests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            password="password",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="password",
        )
        self.post = Post.objects.create(
            author=self.author,
            title="First post",
            content="First content",
        )

    def test_anonymous_user_can_view_posts(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.post.title)

    def test_anonymous_user_cannot_create_post(self):
        response = self.client.post(
            reverse("post-list"),
            {
                "title": "New post",
                "content": "New content",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.post(
            reverse("post-list"),
            {
                "title": "New post",
                "content": "New content",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.latest("id").author, self.author)

    def test_author_can_update_own_post(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.patch(
            reverse("post-detail", kwargs={"pk": self.post.pk}),
            {"title": "Updated title"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated title")

    def test_user_cannot_update_another_users_post(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            reverse("post-detail", kwargs={"pk": self.post.pk}),
            {"title": "Hacked title"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "First post")

    def test_author_can_delete_own_post(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.delete(
            reverse("post-detail", kwargs={"pk": self.post.pk}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_like_action_toggles_like(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("post-like", kwargs={"pk": self.post.pk})

        create_response = self.client.post(url)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Like.objects.filter(user=self.other_user, post=self.post).exists()
        )

        delete_response = self.client.post(url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Like.objects.filter(user=self.other_user, post=self.post).exists()
        )
