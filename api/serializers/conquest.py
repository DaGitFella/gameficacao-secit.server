from rest_framework import serializers

from api.models.conquest import Conquest
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.stamp import StampSerializer


# class ConquestListSerializer(serializers.ListSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def to_representation(self, instance):
#         print("passou por mim! ConquestListSerializer")
#         print()
#         print(instance)
#         print()
#         print(type(instance))
#         return super().to_representation(instance)
#
#     def __iter__(self):
#         self.generator = iter(self.initial_data)
#         return self.generator
#
#     def __next__(self):
#         return next(self.generator)


class ConquestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conquest
        fields = ['name', 'color', 'required_stamps', 'min_stamp_types_amount', 'stamps']
        list_serializer_class = CustomListSerializer

    stamps = StampSerializer(many=True)

    # def to_internal_value(self, data):
    #     return {
    #         'name': data['name'],
    #         'color': data['color'],
    #         'required_stamps': data['required_stamps'],
    #         'min_stamp_types_amount': data['min_stamp_types_amount'],
    #         'stamps': StampSerializer(many=True, data=data['stamps'])
    #     }

    # def validate(self, **kwargs):
    #     pass

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
