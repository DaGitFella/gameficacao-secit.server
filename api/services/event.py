from api.models import Event
from api.models.conquest import Conquest
from api.models.stamp import Stamp
from api.services.activity import ActivityService
from api.services.award import AwardService
from api.services.conquest import ConquestService
from api.services.stamp import StampService


class EventService:
    @staticmethod
    def create(serializer):
        event_data = serializer.validated_data
        event = Event(
            name=event_data['name'],
            year=event_data['year'],
            edition_number=event_data['edition_number'],
            user_who_created=event_data['user_who_created'],
        )

        Event.objects.save(event)

        print("--- event_data['conquests'] in EventService ---")
        print(event_data['conquests'])
        print()

        conquests = ConquestService.create_from_data_list(event, event_data['conquests'])
        event_data = EventService.put_conquests_entities_in_data(conquests, event_data)

        print("--- conquests in EventService ---")
        print(conquests)
        print()

        print('\n--- event_data["activities"] in EventService.create before Stamps ---')
        print(event_data["activities"])
        print()
        print(event_data["stamps"])
        print()

        stamps = StampService.create_from_data_list(event_data['stamps'])
        event_data = EventService.put_stamps_entities_in_activities_data(stamps, event_data)

        print('\n--- event_data in EventService.create before Activities ---')
        print(event_data["activities"])
        print()
        print(event_data["awards"])
        print()

        ActivityService.create_from_data_list(event, event_data['activities'])

        print('\n--- event_data in EventService.create before Awards ---')
        print(event_data["activities"])
        print()
        print(event_data["awards"])
        print()
        AwardService.create_from_serializer(event, event_data['awards']),

        return event

    @staticmethod
    def put_conquests_entities_in_data(conquests: list[Conquest], event_data: dict):
        conquests_data = [
            {'conquest': conquest, 'stamps': conquest_data['stamps']}
            for conquest, conquest_data in zip(conquests, event_data['conquests'])
        ]

        stamps = []
        for stamps_data in conquests_data:
            stamps.extend([
                {'stamp': stamp_data, 'conquest': stamps_data['conquest']}
                for stamp_data in stamps_data['stamps']
            ])

        return {**event_data, 'stamps': stamps}

    @staticmethod
    def put_stamps_entities_in_activities_data(stamps: list[Stamp], event_data: dict):
        stamps = [
            StampService.get_by_icon(activity_data['stamp']['icon'], stamps)
            for activity_data in event_data['activities']
        ]

        activities = [
            {**activity_data, "stamp": stamp}
            for activity_data, stamp in zip(event_data['activities'].data, stamps)
        ]

        print('\n--- activities in EventService.put_stamps_entities_in_activities_data ---')
        print(activities)
        print()

        return {**event_data, 'activities': activities}

    @staticmethod
    def raise_if_invalid_conquests(conquests_data):
        raise NotImplementedError()

    @staticmethod
    def raise_if_invalid_awards(awards_data):
        raise NotImplementedError()

    @staticmethod
    def raise_if_invalid_activities(activities_data):
        raise NotImplementedError()
