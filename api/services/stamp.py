from functools import reduce

from api.models.conquest import Conquest
from api.models.stamp import Stamp


class StampService:
    @staticmethod
    def create_from_data_list(data_list):
        return Stamp.objects.save(
            [StampService.create(data["stamp"], data["conquest"]) for data in data_list]
        )

    @staticmethod
    def create_from_serializer(serializer, conquest: Conquest):
        return StampService.create(serializer.data, conquest)

    @staticmethod
    def create(data, conquest: Conquest):
        return Stamp(icon=data['icon'], conquest=conquest)

    @staticmethod
    def get_from_event_data(data: dict):
        return reduce(
            lambda s1, s2: s1 + s2,
            map(lambda c: c['stamps'], data['conquests'])
        )

    @staticmethod
    def get_by_icon(stamp_icon: str, stamps: list[Stamp]):
        return next(filter(lambda stamp: stamp.icon == stamp_icon, stamps))
