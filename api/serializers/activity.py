from rest_framework import serializers

from api.models.activity import Activity
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.stamp import StampSerializer


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['stamps_amount', 'type', 'stamp']
        list_serializer_class = CustomListSerializer

    stamp = StampSerializer()
