from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Event
from api.models.activity import Activity
from api.tests.event_environment_manager import EventEnvironmentManager
from api.tests import BASE_URL
from api.tests.user_environment_manager import UserEnvironmentManager
from api.serializers.event import EventSerializer

class EventTestCase(APITestCase):
    event_manager = EventEnvironmentManager()
    user_manager = UserEnvironmentManager()

    def test_post__on_happy_path__should_return_CREATED(self):
        self.event_manager.set_database_environment({"secit-2024": False})

        response = self.client.post(f"{BASE_URL}/events", self.event_manager.get_data("secit-2024"), headers=self.user_manager.get_credentials("admin-user"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.event_manager.retrieve("secit-2024"))

    def test_get__created_events_on_happy_path__should_return_OK(self):
        self.event_manager.set_database_environment({"secit-2024": True, "sipex-2024": True})

        response = self.client.get(f"{BASE_URL}/events?created=true", headers=self.user_manager.get_credentials("admin-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data[0])

    def test_get__created_events_with_common_credentials__should_return_FORBIDDEN(self):
        self.user_manager.set_database_environment({"common-user": True})

        response = self.client.get(f"{BASE_URL}/events?created=true", headers=self.user_manager.get_credentials("common-user"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get__participated_events_on_happy_path__should_return_OK(self):
        # print(self.event_manager.get_data("secit-202"))
        self.event_manager.set_database_environment({"secit-2024": True, "sipex-2024": True})
        self.user_manager.set_database_environment({"common-user": True})

        response = self.client.get(f"{BASE_URL}/events", headers=self.user_manager.get_credentials("common-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EventSerializerTestCase(APITestCase):
    event_manager = EventEnvironmentManager()
    user_manager = UserEnvironmentManager()
    serializer = EventSerializer()

    def test_create__on_happy_path__should_return_OK(self):
        self.event_manager.set_database_environment({"secit-2024": False})
        event_data = self.event_manager.get_data("secit-2024")
        event_data.update({"user": self.user_manager.retrieve_user("admin-user")})

        event = self.serializer.create(event_data)

        self.assertIsInstance(event, Event)
        self.assertIsInstance(event.activities.all()[0], Activity)
