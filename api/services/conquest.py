from api.models.conquest import Conquest


class ConquestService:
    @staticmethod
    def create_from_data_list(event, data_list) -> list[Conquest]:
        # return Conquest.objects.save(list(map(lambda d: ConquestService.create(event, d), data)))
        print('--- map result in ConquestService ---')
        print([ConquestService.create(event, data) for data in data_list])
        print(type(data_list))
        print()
        return Conquest.objects.save(
            [ConquestService.create(event, data) for data in data_list]
        )

    @staticmethod
    def create(event, data):
        conquest = Conquest(
            name=data['name'],
            color=data['color'],
            required_stamps=data['required_stamps'],
            min_stamp_types_amount=data['min_stamp_types_amount'],
            event=event,
        )

        # conquest.stamps.set(StampService.create_from_list(data['stamps']))

        return conquest
