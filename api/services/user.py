from api.models.user import User
from api.serializers.user import UserSerializer


class UserService:
    @staticmethod
    def get_from_serializer(serializer: UserSerializer):
        return User.objects.get(username=serializer.data['username'])

    @staticmethod
    def get_from_pk(pk):
        return User.objects.get(pk=pk)

    @staticmethod
    def get_serializer_from_pk(pk):
        user = UserService.get_from_pk(pk)
        serializer = UserSerializer(user)

        print("inside UserService")
        print(user, user.username, user.name)
        print(serializer)
        print()

        return serializer
