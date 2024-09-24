from api.models import Event
from api.services.activity import ActivityService
from api.services.award import AwardService
from api.services.conquest import ConquestService


class EventService:
    @staticmethod
    def create(serializer):
        event_data = serializer.data
        event = Event(
            name=serializer.data.name,
            year=serializer.data.year,
            edition_number=serializer.data.edition_number
        )
        event.user_who_created = event_data.user_who_created

        event.conquests = ConquestService.create_from_serializer_list(event_data.conquests)
        event.awards = AwardService.create_from_serializer_list(event_data.awards)
        event.activities = ActivityService.create_from_serializer_list(event_data.activities)

        return event

    @staticmethod
    def raise_if_invalid_conquests(conquests_data):
        raise NotImplementedError()

    @staticmethod
    def raise_if_invalid_awards(awards_data):
        raise NotImplementedError()

    @staticmethod
    def raise_if_invalid_activities(activities_data):
        raise NotImplementedError()
