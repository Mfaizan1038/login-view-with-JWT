from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserAPITests(APITestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(
            username="faizan",
            email="faizan@example.com",
            password="test123",
            phone_number="123456789",
        )
        self.user2 = User.objects.create_user(
            username="ali",
            email="ali@example.com",
            password="test123",
            phone_number="987654321",
        )

      
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.refresh_url = "/api/refresh/"
        self.logout_url = "/api/logout/"
        self.user_list_url = "/api/users/"
        self.user_search_url = "/api/search/"
        self.user_ordering_url = "/api/ordering/"

    
    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass123",
            "confirm_password": "pass123",
            "phone_number": "12345",
        }
        response = self.client.post(self.register_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_login_user(self):
        data = {"username": "faizan", "password": "test123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    #
    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user1)
        data = {"refresh": str(refresh)}
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    
    def test_logout_user(self):
        refresh = RefreshToken.for_user(self.user1)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {"refresh": str(refresh)}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

   
    def test_user_filtering(self):
        
        url = f"{self.user_list_url}?username=faizan"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if "results" in response.data:
            self.assertEqual(len(response.data["results"]), 1)
        else:
            self.assertEqual(len(response.data), 1)

    
    def test_user_search(self):
       
        url = f"{self.user_search_url}?search=ali"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if "results" in response.data:
            self.assertGreaterEqual(len(response.data["results"]), 1)
        else:
            self.assertGreaterEqual(len(response.data), 1)

    
    def test_user_ordering(self):
        url = f"{self.user_ordering_url}?ordering=username"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if "results" in response.data:
            usernames = [u["username"] for u in response.data["results"]]
        else:
            usernames = [u["username"] for u in response.data]
        self.assertEqual(usernames, sorted(usernames))
