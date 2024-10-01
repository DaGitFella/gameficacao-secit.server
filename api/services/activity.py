from api.managers.activity import ActivityManager
from api.models.activity import Activity
from api.serializers.activity import ActivitySerializer
from api.services.stamp import StampService


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
    def raise_if_invalid(activities):
        pass