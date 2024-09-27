from api.models.award import Award


class AwardService:
    @staticmethod
    def create_from_serializer(event, data):
        return Award.objects.save(list(map(lambda d: AwardService.create(event, d), data)))

    # @staticmethod
    # def create_from_serializer(serializer):
    #     return AwardService.create(event, serializer.data)

    @staticmethod
    def create(event, data):
        award = Award(
            description=data['description'],
            required_conquests=data['required_conquests'],
            max_quantity=data['max_quantity'],
            available_quantity=data['available_quantity'],
            event=event,
        )

        return award
