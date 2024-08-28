from rest_framework import serializers

from api.models.conquest import Conquest
from api.serializers.stamp import StampSerializer

class ConquestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conquest
        fields = ['number', 'year', 'edition_number']

    def create_from_list(self, validated_data):
        conquests = []
        stamps = []
        for conquest_data in validated_data['conquests']:
            conquest_data.update({"event": validated_data['event']})

            conquest_data_without_stamps = conquest_data.copy()
            conquest_data_without_stamps.pop('stamps', None)
            conquest = self.create(conquest_data_without_stamps)
            conquests.append(conquest)

            for stamp_data in conquest_data['stamps']:
                stamp_data.update({"event": conquest_data['event']})
                stamp_data.update({"conquest": conquest})
                stamps.append(StampSerializer().create(stamp_data))

        return {'created_conquests': conquests, 'created_stamps': stamps}

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
