from rest_framework import serializers

from api.models.stamp import Stamp
from api.serializers.custom_list_serializer import CustomListSerializer


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['icon']
        list_serializer_class = CustomListSerializer
