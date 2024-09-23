from api.models.stamp import Stamp
from api.serializers.stamp import StampSerializer


class StampService:
    @staticmethod
    def create_from_serializer_list(serializer: StampSerializer):
        return list(map(StampService.create, serializer.data))

    @staticmethod
    def create_from_serializer(serializer: StampSerializer):
        return StampService.create(serializer.data)

    @staticmethod
    def create(data):
        stamp = Stamp(icon=data['icon'])
        return stamp
