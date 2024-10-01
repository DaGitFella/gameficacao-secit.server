from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers.event import EventSerializer
from api.tests import BASE_URL
from api.tests.event_environment_manager import EventEnvironmentManager
from api.tests.user_environment_manager import UserEnvironmentManager
from pprint import pprint

class EventTestCase(APITestCase):
    event_manager = EventEnvironmentManager()
    user_manager = UserEnvironmentManager()

    def test_post__on_happy_path__should_return_CREATED(self):
        self.event_manager.set_database_environment({"secit-2024": False})
        data = self.event_manager.get_data("secit-2024")

        response = self.client.post(f"{BASE_URL}/events", data,
                                    headers=self.user_manager.get_credentials("admin-user"), format="json")

        self.event_manager.update_data_ids({"secit-2024": response.data["id"]})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        print("\n" * 4)
        print('--- response.data in EventTestCase test_post__on_happy_path ---')
        print(response.data)

        print(response.data['user_who_created'])
        admin_user: dict = self.user_manager.get_user_data("admin-user")
        admin_user.pop("password")

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['user_who_created'], admin_user)
        self.assertEqual(response.data['conquests'], data['conquests'])
        self.assertEqual(response.data['activities'], data['activities'])

        received_awards = [
            {
                "description": award["description"],
                "required_conquests": award["required_conquests"],
                "max_quantity": award["max_quantity"],
            }

            for award in response.data['awards']
        ]

        print()
        print(received_awards)
        print(data['awards'])

        self.assertEqual(received_awards, data['awards'])

    def test_get__created_events_on_happy_path__should_return_OK(self):
        self.event_manager.set_database_environment({"secit-2024": True, "sipex-2024": True})

        response = self.client.get(f"{BASE_URL}/events?created=true",
                                   headers=self.user_manager.get_credentials("admin-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data[0])

    def test_get__created_events_with_common_credentials__should_return_FORBIDDEN(self):
        self.user_manager.set_database_environment({"common-user": True})

        response = self.client.get(f"{BASE_URL}/events?created=true",
                                   headers=self.user_manager.get_credentials("common-user"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get__participated_events_on_happy_path__should_return_OK(self):
        self.event_manager.set_database_environment({"secit-2024": True, "sipex-2024": True})
        self.user_manager.set_database_environment({"common-user": True})

        response = self.client.get(f"{BASE_URL}/events", headers=self.user_manager.get_credentials("common-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventSerializerTestCase(APITestCase):
    event_manager = EventEnvironmentManager()
    user_manager = UserEnvironmentManager()

    # conquests->color must be a valid hex color code
    def test_conquest_is_valid__invalid_conquest_color__should_return_false(self):
        data = self.event_manager.get_data("secit-2024")
        data["conquests"] = [
            {**conquest, "color": "NotHex"}
            for conquest in data["conquests"]
        ]

        self.user_manager.set_database_environment({"admin-user": True})
        data["user_who_created"] = self.user_manager.retrieve_user("admin-user").id

        serializer = EventSerializer(data=data)
        is_valid = serializer.is_valid()

        print("--- serializer.errors in EventSerializerTestCase."
              "test_conquest_is_valid__invalid_conquest_color__should_return_false ---")
        print(serializer.errors)

        self.assertFalse(is_valid)

    # conquests->stamps->icon must be unique inside event
    def test_conquest_is_valid__not_unique_stamps_icons__should_return_false(self):
        data = self.event_manager.get_data("secit-2024")
        data["conquests"] = [
            {
                **conquest,
                "stamps": [{"icon": "bad-and-not-unique-filename.png"}] * len(conquest["stamps"])
            }
            for conquest in data["conquests"]
        ]

        self.user_manager.set_database_environment({"admin-user": True})
        data["user_who_created"] = self.user_manager.retrieve_user("admin-user").id

        serializer = EventSerializer(data=data)
        is_valid = serializer.is_valid()

        print("--- serializer.errors in EventSerializerTestCase."
              "test_conquest_is_valid__not_unique_stamps_icons__should_return_false ---")
        pprint(serializer.errors)

        self.assertFalse(is_valid)

    # activities->stamp must be declared before, in conquests->stamps
    def test_activities_is_valid__non_existent_stamp_icon__should_return_false(self):
        data = self.event_manager.get_data("secit-2024")
        data["activities"] = [
            {
                **activity,
                "stamp": {"icon": "non-existent-filename.png"}
            }
            for activity in data["activities"]
        ]

        self.user_manager.set_database_environment({"admin-user": True})
        data["user_who_created"] = self.user_manager.retrieve_user("admin-user").id

        serializer = EventSerializer(data=data)
        is_valid = serializer.is_valid()

        print("--- serializer.errors in EventSerializerTestCase."
              "test_award_is_valid__non_existent_stamp_icon__should_return_false ---")
        pprint(object=serializer.errors, indent=4)

        self.assertFalse(is_valid)