from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.api.serializers import ProfileDisplaySerializer


class CurrentProfileAPIView(APIView):
    """
    A simple view to fetch a profile info
    """

    def get(self, request):
        serializer = ProfileDisplaySerializer(request.user)
        return Response(serializer.data)
