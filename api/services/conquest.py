from api.models.conquest import Conquest
from api.services.stamp import StampService


class ConquestService:
    @staticmethod
    def create_from_data_list(event, data):
        return Conquest.objects.save(list(map(lambda d: ConquestService.create(event, d), data)))

    @staticmethod
    def create(event, data):
        conquest = Conquest(
            name=data['name'],
            color=data['color'],
            required_stamps=data['required_stamps'],
            min_stamp_types_amount=data['min_stamp_types_amount'],
            event=event,
        )

        conquest.stamps.set(StampService.create_from_serializer_list(data['stamps']))

        return conquest
