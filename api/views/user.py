from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers.user import UserSerializer


class UserView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            return Response(user, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def put(request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def delete(request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            serializer.delete(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def set_role(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        if request.user.role == User.Roles.ADMIN:
            if not request.data['role'] in User.Roles:
                return Response(f'Role must be one of "{User.Roles}"', status=status.HTTP_400_BAD_REQUEST)

            serializer.set_role(role=request.data['role'], username=request.data['username'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
