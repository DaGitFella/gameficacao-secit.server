from django.template.context_processors import static
from rest_framework import serializers

from api.models.stamp import Stamp

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['icon', 'event', 'conquest']

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
        return Stamp.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
