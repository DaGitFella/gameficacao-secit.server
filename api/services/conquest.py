from api.models.conquest import Conquest
from api.serializers.conquest import ConquestSerializer
from api.services.stamp import StampService


class ConquestService:
    @staticmethod
    def create_from_serializer_list(serializer: ConquestSerializer):
        data = serializer.data
        return list(map(ConquestService.create, data))

    @staticmethod
    def create(data):
        conquest = Conquest(
            name=data['name'],
            color=data['color'],
            required_stamps=data['required_stamps'],
            min_stamps_amount=data['min_stamps_amount'],
        )

        conquest.stamps = StampService.create_from_serializer_list(data['stamps'])

        return conquest
