from rest_framework import serializers

from api.models.user import User
from gameficacao_secit_server import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def save(self):
        if self.validated_data['email'] == settings.ADMIN_EMAIL:
            self.Meta.model.objects.create_superuser(
                name=self.validated_data['name'],
                email=self.validated_data['email'],
                password=self.validated_data['password'],
                username=self.validated_data['username']
            )
        else:
            self.Meta.model.objects.create_user(
                name=self.validated_data['name'],
                email=self.validated_data['email'],
                password=self.validated_data['password'],
                username=self.validated_data['username']
            )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation
