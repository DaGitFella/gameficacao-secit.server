from rest_framework import serializers

from api.models.conquest import Conquest
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.stamp import StampSerializer


class ConquestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conquest
        fields = ['name', 'color', 'required_stamps', 'min_stamp_types_amount', 'stamps']
        list_serializer_class = CustomListSerializer

    stamps = StampSerializer(many=True)

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
