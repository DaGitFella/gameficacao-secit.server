from rest_framework import serializers

from api.models.user import User
from gameficacao_secit_server import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name']

    def create(self, validated_data):
        data = {
            'name': validated_data['name'],
            'email': validated_data['email'],
            'password': validated_data['password'],
            'username': validated_data['username']
        }

        if validated_data['email'] == settings.ADMIN_EMAIL:
            return self.Meta.model.objects.create_superuser(**data)

        return self.Meta.model.objects.create_user(**data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation

    def update(self, instance: User, validated_data):
        return self.Meta.model.objects.update(instance, validated_data)

    def delete(self, user: User):
        self.Meta.model.objects.delete(user)

    def set_role(self, role: str, username: str):
        self.Meta.model.objects.set_role(role=role, username=username)
