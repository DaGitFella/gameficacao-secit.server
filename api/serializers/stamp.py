from django.template.context_processors import static
from rest_framework import serializers

from api.models.stamp import Stamp
from api.serializers.custom_list_serializer import CustomListSerializer


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['icon']
        list_serializer_class = CustomListSerializer

    @staticmethod
    def create_serializers_from_lists(conquests, conquests_serializers):
        stamps_serializers = []
        for conquest, serializer in zip(conquests, conquests_serializers):
            for stamp in conquest['stamps']:
                stamp['conquest'] = serializer
                stamps_serializers.append(StampSerializer(data=stamp))

        return stamps_serializers

    @staticmethod
    def get_data_from_lists(conquests, conquests_serializers):
        stamps = []
        for conquest, serializer in zip(conquests, conquests_serializers):
            for stamp in conquest['stamps']:
                stamp['conquest'] = serializer
                stamps.append(stamp)

        return stamps

    def create(self, validated_data):
        return Stamp.objects.save_in_db(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('conquest')
    #     return representation
