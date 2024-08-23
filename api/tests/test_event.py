from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.event_environment_manager import EventEnvironmentManager
from api.tests import BASE_URL
from api.tests.user_environment_manager import UserEnvironmentManager


class EventTestCase(APITestCase):
    event_manager = EventEnvironmentManager()
    user_manager = UserEnvironmentManager()

    def test_get__on_happy_path__should_return_OK(self):
        self.event_manager.set_database_environment({"secit-2024": True, "sipex-2024": True})

        response = self.client.get(f"{BASE_URL}/events?created=true", headers=self.user_manager.get_credentials("admin-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data[0])
