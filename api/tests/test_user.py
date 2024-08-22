from rest_framework import status
from rest_framework.test import APITestCase

from api.tests import BASE_URL
from api.tests.user_environment_manager import UserEnvironmentManager


class UserTestCase(APITestCase):
    environment_manager = UserEnvironmentManager()

    def test_post__on_happy_path__should_return_CREATED(self):
        self.environment_manager.set_database_environment({"common-user": False})
        response = self.client.post(f"{BASE_URL}/users", self.environment_manager.get_user_data("common-user"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post__with_repeated_fields__should_return_BAD_REQUEST(self):
        self.environment_manager.set_database_environment({"common-user": True})
        response = self.client.post(f"{BASE_URL}/users", self.environment_manager.get_user_data("common-user"))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login__on_happy_path__should_return_OK(self):
        self.environment_manager.set_database_environment({"common-user": True})
        response = self.client.post(f"{BASE_URL}/token", self.environment_manager.get_user_login_data("common-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login__with_wrong_password__should_return_OK(self):
        self.environment_manager.set_database_environment({"common-user": True})

        login_data = self.environment_manager.get_user_login_data("common-user")
        login_data["password"] = "wrong passord"

        response = self.client.post(f"{BASE_URL}/token", login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get__on_happy_path__should_return_OK(self):
        self.environment_manager.set_database_environment({"common-user": True})
        response = self.client.get(f"{BASE_URL}/users", headers=self.environment_manager.get_credentials("common-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)
        self.assertNotIn("password", response.data)

    def test_put__on_happy_path__should_return_NO_CONTENT(self):
        self.environment_manager.set_database_environment({"common-user": True})
        edited_data = self.environment_manager.get_user_data("common-user")
        edited_data["name"] = "Another Common User"

        response = self.client.put(f"{BASE_URL}/users",
                                   edited_data,
                                   headers=self.environment_manager.get_credentials("common-user"))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = self.environment_manager.retrieve_user("common-user")
        self.assertEqual(user.name, edited_data["name"])

    def test_put__with_repeated_values__should_return_BAD_REQUEST(self):
        self.environment_manager.set_database_environment({"common-user": True, "admin-user": True})
        edited_data = self.environment_manager.get_user_data("common-user")
        edited_data["email"] = self.environment_manager.get_user_data("admin-user")["email"]

        response = self.client.put(f"{BASE_URL}/users",
                                   edited_data,
                                   headers=self.environment_manager.get_credentials("common-user"))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        self.environment_manager.set_database_environment({"common-user": True})
        response = self.client.delete(f"{BASE_URL}/users",
                                      headers=self.environment_manager.get_credentials("common-user"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.environment_manager.does_user_exist("common-user"))

    def test_set_role__on_happy_path__should_return_NO_CONTENT(self):
        self.environment_manager.set_database_environment({"common-user": True, "admin-user": True})

        response = self.client.post(f"{BASE_URL}/users/set_role",
                                    {"role": "admin", "username": "common-user"},
                                    headers=self.environment_manager.get_credentials("admin-user"))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_set_role__with_invalid_role__should_return_NO_CONTENT(self):
        self.environment_manager.set_database_environment({"common-user": True, "admin-user": True})

        response = self.client.post(f"{BASE_URL}/users/set_role",
                                    {"role": "non-existent", "username": "common-user"},
                                    headers=self.environment_manager.get_credentials("admin-user"))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
