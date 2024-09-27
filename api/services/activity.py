from api.managers.activity import ActivityManager
from api.models.activity import Activity
from api.services.stamp import StampService


class ActivityService:
    @staticmethod
    def create_from_data_list(event, data_list):
        return Activity.objects.save(list(map(lambda data: ActivityService.create(event, data), data_list)))

    @staticmethod
    def create(event, data):
        activity = Activity(
            stamps_amount=data['stamps_amount'],
            type=data['type'],
            event=event,
            stamp=data['stamp']
        )

        return activity
