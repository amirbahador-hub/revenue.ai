from rest_framework.response import Response
from rest_framework.views import APIView


class TestCore(APIView):
    def get(self, request, *args, **kwargs):
        temp_result = {
            "results": {
                "title": "Hi",
            }
        }
        return Response(temp_result)
