from rest_framework import serializers

from api.models.stamp import Stamp

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['number', 'year', 'edition_number']

    # def create_from_list(self, validated_data):
    #     stamps = []
    #     for conquest in validated_data['conquests']:
    #         for stamp in conquest['stamps']:
    #             stamp.update({"event": validated_data['event']})
    #             stamps.append(self.create(stamp))
    #
    #     return stamps

    def create(self, validated_data):
        return Stamp.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
