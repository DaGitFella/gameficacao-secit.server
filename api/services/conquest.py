import re
from collections import Counter
from functools import reduce
from pprint import pprint

from api.models.conquest import Conquest


class ConquestService:
    @staticmethod
    def create_from_data_list(event, data_list) -> list[Conquest]:
        print('--- map result in ConquestService ---')
        print([ConquestService.create(event, data) for data in data_list])
        print(type(data_list))

        for data in data_list:
            print(data, end=" | ")

        print()
        return Conquest.objects.save(
            [ConquestService.create(event, data) for data in data_list]
        )

    @staticmethod
    def create(event, data):
        return Conquest(
            name=data['name'],
            color=data['color'],
            required_stamps=data['required_stamps'],
            min_stamp_types_amount=data['min_stamp_types_amount'],
            event=event,
        )

    @staticmethod
    def validate_all(conquests: list[dict]):
        errors = [
            {"stamps": validation_data["detail"]} if not validation_data["is_valid"] else {}
            for validation_data in ConquestService.validate_stamps_icon_unicity(conquests)
        ]

        REDUCE_RESULT = reduce(lambda e1, e2: (e1 == {} or e1) and e2 == {}, errors)
        print('\n--- errors in ConquestService.validate ---')
        pprint(errors)
        print(f'reduce result: {REDUCE_RESULT}')
        print()


        if REDUCE_RESULT:
            errors = []

        return errors

    @staticmethod
    def validate_stamps_icon_unicity(conquests: list[dict]) -> list:
        INVALID_VALIDATION_DATA = {"is_valid": False, "detail": "Icons filenames must be unique for the same event."}
        VALID_VALIDATION_DATA = {"is_valid": True, "detail": None}

        icons = ConquestService.get_icons_from_conquests(conquests)
        has_duplicates = len(set(icons)) != len(icons)

        if has_duplicates:
            counter = Counter(icons)
            duplicated_icons = [icon for icon in counter.keys() if counter[icon] > 1]

            invalid_conquests_ids = [
                i for i, conquest in enumerate(conquests)
                if ConquestService.conquest_has_icons(conquest, duplicated_icons)
            ]

            return [
                INVALID_VALIDATION_DATA if i in invalid_conquests_ids else VALID_VALIDATION_DATA
                for i in range(len(conquests))
            ]

        return [VALID_VALIDATION_DATA] * len(conquests)

    @staticmethod
    def get_icons_from_conquests(conquests: list[dict]) -> list[str]:
        stamps = reduce(
            lambda s1, s2: s1 + s2,
            [conquest["stamps"] for conquest in conquests],
        )

        icons = [stamp["icon"] for stamp in stamps]
        return icons

    @staticmethod
    def conquest_has_icons(conquest: dict, icons: list) -> bool:
        conquest_icons = [stamp["icon"] for stamp in conquest["stamps"]]

        # print(conquest_icons, icons, sep=" -=|-|-|=- ")
        # print(set(conquest_icons).intersection(set(icons)))
        # print()

        return set(conquest_icons).intersection(set(icons)) != set()

    @staticmethod
    def validate_color(value: str) -> dict:
        REGEX_HEX_COLOR_CODE = r"[0-9A-Fa-f]{6}"
        match = re.search(REGEX_HEX_COLOR_CODE, value)
        if not match:
            return {"is_valid": False, "detail": "Color must be an hex string of six characters."}

        return {"is_valid": True, "detail": None}
