from api.models.activity import Activity
from api.services.stamp import StampService


class ActivityService:
    @staticmethod
    def create_from_serializer_list(serializer):
        data = serializer.data
        return list(map(ActivityService.create, data))

    @staticmethod
    def create(data):
        activity = Activity(
            stamps_amount=data['stamps_amount'],
            timestamp=data['timestamp'],
            type=data['type'],
        )

        activity.stamp = StampService.create_from_serializer(data['stamp'])

        return activity
