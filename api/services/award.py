from api.models.award import Award


class AwardService:
    @staticmethod
    def create_from_data_list(event, data_list):
        return Award.objects.save(
            [AwardService.create(event, data) for data in data_list],
        )

    @staticmethod
    def create(event, data):
        return Award(
            description=data['description'],
            required_conquests=data['required_conquests'],
            max_quantity=data['max_quantity'],
            available_quantity=data['max_quantity'],
            event=event,
        )
