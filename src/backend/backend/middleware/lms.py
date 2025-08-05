import requests
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from backend.middleware.serializers import *
from backend.middleware.utils import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from backend.base.models import RequestLog
from backend.base.models import Terminal
from backend.base.models import PublicIncIndexes


class LMLAuthRegister(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LMSAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("serializer.is_valid() : ", serializer.is_valid())
        data = serializer.validated_data
        print("serializer.validated_data : ", serializer.validated_data)
        body = {
            "posCode": data.get("posCode"),
            "branchCode": data.get("branchCode"),
            "merchantTtd": data.get("merchantTtd", ""),
            "name": data.get("name", "")
        }
        url = settings.LOYALTY_URL + "/auth/register"
        response = requests.post(url, json=body)
        return Response(response.json())


class LMLCheckStatus(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("request.data : ", request.data)
        serializer = LMSAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "posCode": data.get("posCode"),
            "branchCode": data.get("branchCode"),
            "merchantTtd": data.get("merchantTtd", ""),
            "name": data.get("name", "")
        }
        url = settings.LOYALTY_URL + "/auth/checkStatus"
        response = requests.put(url, headers=headers, json=body)
        print("response : ", response)
        return Response(response.json())

class LMLStartTransaction(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("request.data : ", request.data)
        serializer = LMSAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        self.terminal = Terminal.objects.filter(terminal_pos_no=data.get("pos_no")).first()

        headers = {
            "Content-Type": "application/json"
        }
        headers["Authorization"] = ""

        body = {
            "posCode": data.get("posCode"),
            "branchCode": data.get("branchCode"),
            "merchantTtd": data.get("merchantTtd", ""),
            "name": data.get("name", "")
        }
        url = settings.LOYALTY_URL + "/transaction/start"
        response = requests.put(url, headers=headers, json=body)
        print("response : ", response)
        return Response(response.json())

    # @POST("transaction/start")
    # Call<StartTransactionResponse> postTransactionStart(@Header("Authorization") String token, @Body StartTransactionRequestBody body);
    # @POST("transaction/usePoint")
    # Call<UsePointResponse> postUsePoint(@Header("Authorization") String token, @Body UsePointRequestBody body);
    # @POST("transaction/cancelPoint")
    # Call<Object> postCancelPoint(@Header("Authorization") String token, @Body UsePointRequestBody body);
    # @POST("transaction/useCoupon")
    # Call<UseCouponResponse> postUseCoupon(@Header("Authorization") String token, @Body UseCouponRequestBody body);
    # @POST("transaction/cancelCoupon")
    # Call<Object> postCancelCoupon(@Header("Authorization") String token, @Body UseCouponRequestBody body);
    # @POST("transaction/useVoucher")
    # Call<UseVoucherResponse> postUseVoucher(@Header("Authorization") String token, @Body UseVoucherRequestBody body);
    # @POST("transaction/cancelVoucher")
    # Call<Object> postCancelVoucher(@Header("Authorization") String token, @Body UseVoucherRequestBody body);
    # @POST("transaction/cancelTransaction")
    # Call<Object> postCancelTransaction(@Header("Authorization") String token, @Body UseVoucherRequestBody body);
    # @POST("transaction/finalize")
    # Call<FinalizeTransactionResponse> postTransactionFinalize(@Header("Authorization") String token, @Body FinalizeTransactionRequestBody body);