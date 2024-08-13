from api.models.event import Event

class EventEnvironmentManager:
    events_data = {
        "secit-2024": {
            "id": None,
            "name": "SECIT",
            "year": "2024",
            "edition_number": 10,

        },
        "sipex-2024": {
            "id": None,
            "name": "SIPEX",
            "year": "2024",
            "edition_number": 3
        }
    }

    def set_database_environment(self, environment: dict[str, bool]):
        environment = environment
        actions = {
            True: lambda e: self.create(e),
            False: lambda e: self.delete(e),
        }

        for key, must_create in environment.items():
            actions[must_create](key)

    @staticmethod
    def retrieve(event_id: int):
        return Event.objects.get(id=event_id)

    @staticmethod
    def exists(event_id: int | None) -> bool:
        return event_id and Event.objects.filter(id=event_id).exists()

    def create(self, key: str):
        data = self.events_data[key]
        if self.exists(data["id"]):
            return None

        event = Event.objects.create(data)
        self.events_data[key]["id"] = event.id

    def delete(self, key: str):
        data = self.events_data[key]
        if self.exists(data["id"]):
            return None

        Event.objects.filter(id=data["id"]).delete()
        self.events_data[key]["id"] = None
