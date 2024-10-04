from rest_framework import serializers

from api.models.conquest import Conquest
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.stamp import StampSerializer
from api.services.conquest import ConquestService



class ConquestListSerializer(CustomListSerializer):
    def validate(self, conquests):
        # print("Passing through ConquestSerializer.validate")

        errors = ConquestService.validate_all(conquests)
        if errors:
            raise serializers.ValidationError({"conquests": errors})

        super().validate(conquests)

        return conquests


class ConquestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conquest
        fields = ['name', 'color', 'required_stamps', 'min_stamp_types_amount', 'stamps']
        list_serializer_class = ConquestListSerializer

    stamps = StampSerializer(many=True)

    @staticmethod
    def validate_color(value: str):
        validation_data = ConquestService.validate_color(value)
        if not validation_data["is_valid"]:
            raise serializers.ValidationError(validation_data["detail"])

        return value
