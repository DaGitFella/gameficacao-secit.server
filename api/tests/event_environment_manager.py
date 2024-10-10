import api.models
from api.models.event import Event
from api.serializers.event import EventSerializer
from api.services.event import EventService
from api.tests.user_environment_manager import UserEnvironmentManager
import json

class EventEnvironmentManager:
    user_env_manager = UserEnvironmentManager()

    events_data = {
        "secit-2024": {
            "id": None,
            "name": "SECIT",
            "year": "2024",
            "edition_number": 10,
            "conquests": [
                {"name": "vimfiquei", "color": "1AB43F", "required_stamps": 4, "stamps": [{"icon": "s1.png"}], "min_stamp_types_amount": 1},
                {"name": "apresentador", "color": "AA5AAF", "required_stamps": 1, "stamps": [{"icon": "s2.png"}], "min_stamp_types_amount": 1},
                {"name": "expert", "color": "2EAB6F", "required_stamps": 1, "stamps": [{"icon": "s3a.png"}, {"icon": "s3b.png"}, {"icon": "s3c.png"}, {"icon": "s3d.png"}], "min_stamp_types_amount": 3},
                {"name": "sabido", "color": "4A375B", "required_stamps": 3, "stamps": [{"icon": "s4.png"}], "min_stamp_types_amount": 1},
                {"name": "curioso", "color": "115C4F", "required_stamps": 6, "stamps": [{"icon": "s5a.png"}, {"icon": "s5b.png"}], "min_stamp_types_amount": 2},
            ],
            "awards": [
                {"description": "bottom branco", "required_conquests": 2, "max_quantity": 150},
                {"description": "bottom azul", "required_conquests": 3, "max_quantity": 150},
                {"description": "copo e selo gamer", "required_conquests": 4, "max_quantity": 150},
            ],
            "activities": [
                {"type": "palestra", "stamps_amount": 1, "stamp": {"icon": "s1.png"}},
                {"type": "roda de conversa", "stamps_amount": 1, "stamp": {"icon": "s1.png"}},
                {"type": "mesa redonda", "stamps_amount": 1, "stamp": {"icon": "s1.png"}},
                {"type": "networking", "stamps_amount": 1, "stamp": {"icon": "s1.png"}},
                {"type": "pergunta-dia-1", "stamps_amount": 1, "stamp": {"icon": "s5a.png"}},
                {"type": "pergunta-dia-2", "stamps_amount": 1, "stamp": {"icon": "s5b.png"}},
                {"type": "apresentação", "stamps_amount": 1, "stamp": {"icon": "s2.png"}},
                {"type": "minicurso 4h", "stamps_amount": 1, "stamp": {"icon": "s3a.png"}},
                {"type": "minicurso 2h", "stamps_amount": 1, "stamp": {"icon": "s3a.png"}},
            ]
        },
        "sipex-2024": {
            "id": None,
            "name": "SIPEX",
            "year": "2024",
            "edition_number": 3,
            "conquests": [
                {"name": "voluntario", "color": "1AB43F", "required_stamps": 1, "stamps": [{"icon": "s1a.png"}, {"icon": "s1b.png"}], "min_stamp_types_amount": 1},
                {"name": "apresentador_sipex", "color": "1AB43F", "required_stamps": 1, "stamps": [{"icon": "s2.png"}], "min_stamp_types_amount": 1},
            ],
            "awards": [
                {"description": "bottom branco", "required_conquests": 2, "max_quantity": 150},
                {"description": "bottom azul", "required_conquests": 3, "max_quantity": 150},
                {"description": "copo e selo gamer", "required_conquests": 4, "max_quantity": 150},
            ],
            "activities": [
                {"type": "palestra", "stamps_amount": 1, "stamp": {"icon": "s1a.png"}},
                {"type": "roda de conversa", "stamps_amount": 1, "stamp": {"icon": "s1a.png"}},
                {"type": "mesa redonda", "stamps_amount": 1, "stamp": {"icon": "s1a.png"}},
                {"type": "apresentação", "stamps_amount": 1, "stamp": {"icon": "s2.png"}},
            ]
        },
    }

    def update_data_ids(self, ids: dict[str, int]):
        for event_name, event_id in ids.items():
            self.events_data[event_name]["id"] = event_id

    def get_data(self, event_name: str):
        data = self.events_data[event_name]

        new_data = {}
        for key, item in data.items():
            if isinstance(item, dict):
                new_data[key] = item.copy()
            elif isinstance(item, list):
                new_data[key] = [element.copy() for element in item]
            else:
                new_data[key] = item

        return new_data

    def set_database_environment(self, environment: dict[str, bool]):
        self.user_env_manager.set_database_environment({"admin-user": True})
        user = self.user_env_manager.retrieve_user("admin-user")

        actions = {
            True: lambda e: self.create(e, user),
            False: lambda e: self.delete(e),
        }

        for key, must_create in environment.items():
            actions[must_create](key)

    def retrieve(self, event_name: str) -> Event:
        event_id = self.events_data[event_name]["id"]
        return Event.objects.get(id=event_id)

    @staticmethod
    def exists(event_id: int | None) -> bool:
        return event_id and Event.objects.filter(id=event_id).exists()

    def create(self, key: str, user: api.models.User):
        data = self.get_data(key)
        if self.exists(data["id"]):
            return None

        print(f'--- {key} in EventEnvironmentManager.create ---')
        print(data)
        json_data = json.dumps(data, indent=4)
        print(json_data)
        print()

        data.update({"user_who_created_id": user.id})
        # data_copy = data.copy()
        # data_copy.pop("id")

        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        event = EventService.create(serializer)
        self.events_data[key]["id"] = event.id

    def delete(self, key: str):
        data = self.events_data[key]
        if self.exists(data["id"]):
            return None

        Event.objects.filter(id=data["id"]).delete()
        self.events_data[key]["id"] = None

    def retrieve_all(self):
        pass
