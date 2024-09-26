from api.models.user import User
from api.serializers.user import UserSerializer


class UserService:
    @staticmethod
    def get_from_pk(pk):
        user = User.objects.get(pk=pk)
        return user

    @staticmethod
    def get_serializer_from_pk(pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(User.objects.get(pk=pk))

        print("inside UserService")
        print(user, user.username, user.name)
        print(serializer)
        print()


        return serializer
