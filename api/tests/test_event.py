from rest_framework.test import APITestCase
from event_environment_manager import EventEnvironmentManager

class EventTestCase(APITestCase):
    event_manager = EventEnvironmentManager()

    def test_get__on_happy_path__should_return_OK(self):
        pass
