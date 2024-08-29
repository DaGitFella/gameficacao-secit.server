from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user import UserSerializer

class EventView(APIView):
    @action(detail=True)
    def get(self, request):
        return Response(status=status.HTTP_200_OK)