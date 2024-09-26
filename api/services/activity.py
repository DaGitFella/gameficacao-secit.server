from api.managers.activity import ActivityManager
from api.models.activity import Activity
from api.services.stamp import StampService


class ActivityService:
    @staticmethod
    def create_from_data_list(event, data):
        return Activity.objects.save(list(map(lambda d: ActivityService.create(event, d), data)))

    @staticmethod
    def create(event, data):
        activity = Activity(
            stamps_amount=data['stamps_amount'],
            timestamp=data['timestamp'],
            type=data['type'],
            event=event,
            stamp=StampService.create_from_serializer(data['stamp'])
        )

        return activity
