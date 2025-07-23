import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from backend.terminal.serializers import *
from backend.terminal.terminal_utils import CreateTerminal


class SetTerminalView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get(self, request):
        response = {
            'status': 'ng',
            'response_msg': '',
        }
        serializer = TerminalSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if CreateTerminal(data):
            response["status"] = "ok"
            return Response(response, status=200)
        return Response(response, status=400)
