from api.models.award import Award


class AwardService:
    @staticmethod
    def create_from_serializer(event, data_list):

        print([AwardService.create(event, data) for data in data_list])
        return Award.objects.save(
            # list(map(lambda d: AwardService.create(event, d), data))
            [AwardService.create(event, data) for data in data_list],
        )

        # return Stamp.objects.save(
        #     [StampService.create(data["stamp"], data["conquest"]) for data in data_list]
        # )

    # @staticmethod
    # def create_from_serializer(serializer):
    #     return AwardService.create(event, serializer.data)

    @staticmethod
    def create(event, data):
        return Award(
            description=data['description'],
            required_conquests=data['required_conquests'],
            max_quantity=data['max_quantity'],
            available_quantity=data['max_quantity'],
            event=event,
        )
