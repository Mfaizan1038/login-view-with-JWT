
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.userfactory import UserFactory




class RegisterTests(APITestCase):
    """Tests for user registration endpoint."""
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")

    def test_register_user_success(self):
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "phone_number": "03001234567",
        }
        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User registered")
        self.assertTrue(User.objects.filter(username="new_user").exists())


class LoginTests(APITestCase):
    """Tests for user login endpoint."""
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.user = UserFactory(username="faizan", email="faizan@example.com")

    def test_login_user_success(self):
        data = {"username": self.user.username, "password": "password123"}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class TokenRefreshTests(APITestCase):
    """Tests for token refresh endpoint."""
    def setUp(self):
        self.client = APIClient()
        self.refresh_url = reverse("token_refresh")
        self.user = UserFactory(username="token_user", email="token@example.com")

    def test_refresh_token_success(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            self.refresh_url, {"refresh": str(refresh)}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)


class LogoutTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse("logout")
        self.user = UserFactory(username="logout_user", email="logout@example.com")

    def test_logout_success(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        response = self.client.post(
            self.logout_url, {"refresh": str(refresh)}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["message"], "Logout successful")


class UserSearchTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.search_url = reverse("search")
        self.user = UserFactory(username="faizan", email="faizan@example.com")
        UserFactory.create_batch(5)

    def test_user_search_filter_order(self):
        response = self.client.get(f"{self.search_url}?search=faizan&ordering=username")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        usernames = [u["username"] for u in response.data]
        self.assertTrue(isinstance(usernames, list))
