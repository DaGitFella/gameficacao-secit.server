from api.managers.activity import ActivityManager
from api.managers.award import AwardManager
from api.managers.conquest import ConquestManager
from api.managers.event import EventManager
from api.managers.stamp import StampManager
from api.models import Event
from api.services.activity import ActivityService
from api.services.award import AwardService
from api.services.conquest import ConquestService
from api.services.stamp import StampService


class EventService:
    @staticmethod
    def create(serializer):
        data = serializer.data
        event = Event(
            name=data['name'],
            year=data['year'],
            edition_number=data['edition_number'],
            user_who_created=data['user_who_created'],
        )

        event.save()

        StampService.create_from_event_data(data)
        ConquestService.create_from_data_list(event, data['conquests']),
        AwardService.create_from_data_list(event, data['awards']),
        ActivityService.create_from_data_list(event, data['activities'])

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
