from django.db.models import QuerySet

from api.models import Event
from api.models.conquest import Conquest
from api.models.stamp import Stamp
from api.services.activity import ActivityService
from api.services.award import AwardService
from api.services.conquest import ConquestService
from api.services.stamp import StampService
from api.services.user import UserService


class EventService:
    @staticmethod
    def create(serializer):
        event_data = serializer.validated_data
        print("--- event_data in EventService.create ---")
        print(event_data)
        print()
        print("--- serializer.errors in EventService.create ---")
        print(serializer.errors)
        print()

        # user_who_created = UserService.get_from_pk(event_data["user_who_created_id"])

        event = Event(
            name=event_data['name'],
            year=event_data['year'],
            edition_number=event_data['edition_number'],
            user_who_created=event_data["user_who_created_id"],
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
        print('\n--- event_data["stamps"] in EventService.create before Stamps ---')
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

        print('\n--- event_data["awards"] in EventService.create before Awards ---')
        print(event_data["awards"])
        print()

        awards = AwardService.create_from_data_list(event, event_data['awards']),

        print('\n--- awards in EventService.create after AwardService ---')
        print(awards)
        print()

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

        print("--- stamps in EventService.put_conquests_entities_in_data ---")
        print(stamps)
        print()

        return {**event_data, 'stamps': stamps}

    @staticmethod
    def put_stamps_entities_in_activities_data(stamps: list[Stamp], event_data: dict):
        ordered_stamps = [
            StampService.get_by_icon(activity_data['stamp']['icon'], stamps)
            for activity_data in event_data['activities']
        ]

        activities = [
            {**activity_data, "stamp": stamp}
            for activity_data, stamp in zip(event_data['activities'].data, ordered_stamps)
        ]

        print('\n--- activities in EventService.put_stamps_entities_in_activities_data ---')
        print(activities)
        print()

        return {**event_data, 'activities': activities}

    @staticmethod
    def merge_exceptions_details(first_detail, second_detail):
        keys_in_common = first_detail.keys() & second_detail.keys()
        merged_details = {}

        for key in keys_in_common:
            merged_details[key] = []
            for first, second in zip(first_detail[key], second_detail[key]):
                merged_details[key].append({**first, **second})

            first_detail.pop(key)
            second_detail.pop(key)

        return {**first_detail, **second_detail, **merged_details}

    @staticmethod
    def get_all_from(user, should_get_created_events: bool):
        query_set: QuerySet = Event.objects.get_all_from(user, should_get_created_events)
        return list(query_set)
