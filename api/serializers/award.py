from rest_framework import serializers

from api.models.award import Award


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['description', 'required_conquests', 'max_quantity', 'available_quantity']

    def create_from_list(self, validated_data):
        awards = []
        for award in validated_data['awards']:
            award.update({"event": validated_data['event']})
            awards.append(self.create(award))

        return {'awards': awards}

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
