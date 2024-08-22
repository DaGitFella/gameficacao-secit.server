from rest_framework.test import APITestCase
from event_environment_manager import EventEnvironmentManager
from api.tests import BASE_URL

class EventTestCase(APITestCase):
    event_manager = EventEnvironmentManager()

    def test_get__on_happy_path__should_return_OK(self):
        self.event_manager.set_database_environment({"secit-2024": True})

        self.client.get(f"{BASE_URL}/events")
