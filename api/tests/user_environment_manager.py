from rest_framework.test import APIClient

import api.models
from api.serializers.user import UserSerializer
from api.tests import BASE_URL
from gameficacao_secit_server import settings


class UserEnvironmentManager:
    def __init__(self):
        self.client = APIClient()

    __users_data = {
        "common-user": {
            "name": "Common User",
            "email": "common-user@email.com",
            "password": "pass",
            "username": "common-user"
        },

        "presenter-user": {
            "name": "Presenter User",
            "email": "presenter-user@email.com",
            "password": "pass",
            "username": "presenter-user"
        },

        "volunteer-user": {
            "name": "Volunteer User",
            "email": "volunteer-user@email.com",
            "password": "pass",
            "username": "volunteer-user"
        },

        "admin-user": {
            "name": "Admin User",
            "email": settings.ADMIN_EMAIL,
            "password": "pass",
            "username": "admin-user"
        }
    }


    def set_database_environment(self, environment: dict[str, bool]):
        actions = {
            True: lambda u: self._create_user_if_doesnt_exist(u),
            False: lambda u: self._delete_user_if_exists(u),
        }

        for username, must_create in environment.items():
            actions[must_create](username)

    @staticmethod
    def retrieve_user(username: str) -> api.models.User:
        return api.models.User.objects.get(username=username)

    @staticmethod
    def does_user_exist(username: str) -> bool:
        return api.models.User.objects.filter(username=username).exists()

    def _create_user_if_doesnt_exist(self, username: str):
        if self.does_user_exist(username):
            return None

        serializer = UserSerializer(data=self.__users_data[username])
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

    def _delete_user_if_exists(self, username: str):
        if not self.does_user_exist(username):
            return None

        user = self.retrieve_user(username)
        user.delete()

    def get_credentials(self, username: str):
        login_data = self.get_user_login_data(username)
        response = self.client.post(f'{BASE_URL}/token', login_data)
        return {"Authorization": f'Bearer {response.data["access"]}'}

    def get_user_data(self, username: str):
        return self.__users_data[username].copy()

    def get_user_login_data(self, username: str):
        return {
            "username": username,
            "password": self.__users_data[username]["password"]
        }
