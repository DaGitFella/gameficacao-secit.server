from rest_framework.views import APIView


class EventView(APIView):
    @staticmethod
    def post(request):
        raise NotImplementedError()

    @staticmethod
    def get(request):
        raise NotImplementedError()

    @staticmethod
    def put(request):
        raise NotImplementedError()

    @staticmethod
    def delete(request):
        raise NotImplementedError()
