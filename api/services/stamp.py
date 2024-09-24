from api.models.stamp import Stamp


class StampService:
    @staticmethod
    def create_from_serializer_list(serializer):
        return list(map(StampService.create, serializer.data))

    @staticmethod
    def create_from_serializer(serializer):
        return StampService.create(serializer.data)

    @staticmethod
    def create(data):
        stamp = Stamp(icon=data['icon'])
        return stamp
