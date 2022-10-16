from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, JSONParser
from typing import BinaryIO
import io, csv, pandas as pd


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        return Response(status=204)

class TestCore(APIView):
    parser_classes = (FileUploadParser, )
    def get(self, request, *args, **kwargs):
        temp_result = {
            "results": {
                "title": "Hi",
            }
        }
        return Response(temp_result)
    
    def post(self, request, *args, **kwargs):
        return Response(request.data)
