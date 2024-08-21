from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.user_environment_manager import UserEnvironmentManager
from api.tests import BASE_URL

class UserTestCase(APITestCase):
    environment_manager = UserEnvironmentManager()

    def test_post__on_happy_path__should_return_CREATED(self):
        self.environment_manager.set_database_environment({"common-user": False})
        response = self.client.post(f"{BASE_URL}/users", self.environment_manager.users_data["common-user"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post__with_repeated_fields__should_return_BAD_REQUEST(self):
        self.environment_manager.set_database_environment({"common-user": True})
        response = self.client.post(f"{BASE_URL}/users", self.environment_manager.users_data["common-user"])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login__on_happy_path__should_return_OK(self):
        self.environment_manager.set_database_environment({"common-user": True})

        print(self.environment_manager.get_user_login_data("common-user"))

        response = self.client.post(f"{BASE_URL}/token", self.environment_manager.get_user_login_data("common-user"))

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
