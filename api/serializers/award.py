from rest_framework import serializers

from api.models.award import Award
from api.serializers.custom_list_serializer import CustomListSerializer


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['description', 'required_conquests', 'max_quantity', 'available_quantity']
        list_serializer_class = CustomListSerializer

    def to_internal_value(self, data):
        return {
            "description": data['description'],
            "required_conquests": data['required_conquests'],
            "max_quantity": data['max_quantity'],
            "available_quantity": data['max_quantity'],
        }
