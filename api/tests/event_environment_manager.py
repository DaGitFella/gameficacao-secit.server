from api.models.event import Event


class EventEnvironmentManager:
    events_data = {
        "secit-2024": {
            "id": None,
            "name": "SECIT",
            "year": "2024",
            "edition_number": 10,
            "conquests": [
                {"name": "vimfiquei", "color": "rosa", "required_stamps": 4, "stamps": ["s1.png"]},
                {"name": "apresentador", "color": "azul", "required_stamps": 1, "stamps": ["s2.png"]},
                {"name": "expert", "color": "azul claro", "required_stamps": 1, "stamps": ["s3.png"]},
                {"name": "sabido", "color": "amarelo", "required_stamps": 3, "stamps": ["s4.png"]},
                {"name": "curioso", "color": "cinza", "required_stamps": 6, "stamps": ["s5.png", "s6.png"]},
            ],
            "awards": [
                {"description": "bottom branco", "required_conquests": 2, "max_quantity": 150, "available_quantity": 100},
                {"description": "bottom azul", "required_conquests": 3, "max_quantity": 150, "available_quantity": 120},
                {"description": "copo e selo gamer", "required_conquests": 4, "max_quantity": 150, "available_quantity": 125},
            ],
        },
        "sipex-2024": {
            "id": None,
            "name": "SIPEX",
            "year": "2024",
            "edition_number": 3,
            "conquests": [
                {"name": "voluntario", "color": "vermelho", "required_stamps": 1, "stamps": [{"s1.png"}]},
                {"name": "apresentador", "color": "azul", "required_stamps": 1, "stamps": [{"s2.png"}]},
            ],
            "awards": [
                {"description": "bottom branco", "required_conquests": 2, "max_quantity": 150, "available_quantity": 100},
                {"description": "bottom azul", "required_conquests": 3, "max_quantity": 150, "available_quantity": 120},
                {"description": "copo e selo gamer", "required_conquests": 4, "max_quantity": 150, "available_quantity": 125},
            ],
        },
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
