from api.models.activity import Activity
from api.services.conquest import ConquestService


class ActivityService:
    @staticmethod
    def create_from_data_list(event, data_list):
        return Activity.objects.save(
            [ActivityService.create(event, data) for data in data_list],
        )

    @staticmethod
    def create(event, data):
        return Activity(
            stamps_amount=data['stamps_amount'],
            type=data['type'],
            event=event,
            stamp=data['stamp']
        )

    @staticmethod
    def validate_stamps_icons(conquests: list[dict], activities: list[dict]):
        conquests_icons = ConquestService.get_icons_from_conquests(conquests)
        activities_icons = ActivityService.get_icons_from_activities(activities)

        are_all_valid = set(activities_icons).issubset(set(conquests_icons))
        if are_all_valid:
            return []

        errors = [
            {} if ActivityService.is_activity_valid(activity, conquests_icons)
            else {"stamp": "Stamp icons must be in conquest stamps."}
            for activity in activities
        ]

        print("--- is_activity_valid for each activity in ActivityService.validate_stamps_icons")
        for activity in activities:
            print(ActivityService.is_activity_valid(activity, conquests_icons), end=" | ")
        print()

        return errors

    @staticmethod
    def get_icons_from_activities(activities: list[dict]):
        return [activity["stamp"]["icon"] for activity in activities]

    @staticmethod
    def is_activity_valid(activity: dict, conquests_icons: list[str]) -> bool:
        return activity["stamp"]["icon"] in conquests_icons

    @staticmethod
    def delete_related(event):
        Activity.objects.filter(event_id=event.id).delete()
