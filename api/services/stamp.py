from functools import reduce

from api.models.stamp import Stamp


class StampService:
    @staticmethod
    def create_from_serializer_list(data):
        return list(map(StampService.create, data))

    @staticmethod
    def create_from_serializer(serializer):
        return StampService.create(serializer.data)

    @staticmethod
    def create(data):
        stamp = Stamp(icon=data['icon'])
        return stamp

    @staticmethod
    def create_from_event_data(data: dict):
        stamps = StampService.get_from_event_data(data)
        return Stamp.objects.save(stamps)

    @staticmethod
    def get_from_event_data(data: dict):
        return reduce(
            lambda s1, s2: s1 + s2,
            map(lambda c: c['stamps'], data['conquests'])
        )
