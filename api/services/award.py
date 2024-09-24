from api.models.award import Award


class AwardService:
    @staticmethod
    def create_from_serializer_list(serializer):
        return list(map(AwardService.create, serializer.data))

    @staticmethod
    def create_from_serializer(serializer):
        return AwardService.create(serializer.data)

    @staticmethod
    def create(data):
        award = Award(
            description=data['description'],
            required_conquests=data['required_conquests'],
            max_quantity=data['max_quantity'],
            available_quantity=data['available_quantity'],
        )

        return award
