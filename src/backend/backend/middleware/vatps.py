import json
import requests
import datetime
import logging
import decimal
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication  # or remove for []
from backend.middleware.serializers import *
from backend.middleware.utils import *
from backend.base.consts import *
from backend.base.models import RequestLog
from backend.base.models import Terminal
from backend.base.models import PublicIncIndexes

logger = logging.getLogger("graylog")

session = requests.Session()

class EBarimtReceiptransactionView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = eBarimtReceiptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        client_request_data = data
        
        self.terminal = Terminal.objects.filter(terminal_pos_no=data.get("pos_no")).first()

        today = datetime.date.today()
        self.operation_index = PublicIncIndexes.get_last_index("%s_%s" % (self.terminal.terminal_pos_no, today.strftime("%Y-%m-%d")))
        self.remote_address = get_address()
        self.guur_transaction_url = settings.GUUR_URL + "/api/borluulaltin.medee"

        if data.get("is_ebarimt"):
            self.sync_ebarimt_data(data)

        response = self.sync_guur_txn(data, client_request_data)

        return Response(response.json())
    
    def sync_ebarimt_data(self, data):
        regno = data.get("regno")
        tin = getMerchantTin(regno)
        
        url = settings.EBARIMT_30_URL + "/api/v1/pos/receipt"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + settings.EBARIMT_TOKEN
        }
        if tin:
            data['merchantTin'] = tin
        print("valid data ", data)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

    def sync_guur_txn(self, data, client_request_data):
        headers = {
            "Content-Type": "text/plain",
        }
        if self.terminal.guur_token not in [None, '']:
            "Access-token": self.terminal.guur_token

        # shts_code = data.get("shts_code")
        # pos_num = data.get("pos_num")

        data = {
            "comport": data.get("pump"),
            "hoshuu": data.get("hoshuu"),
            
            "source": data.get("source"),
            "pay_amount": data.get("pay_amount"),
            "discount": data.get("discount"),
            "pos_number": data.get("pos_number"),
            "shts_code": data.get("shts_code"),
            "payment_ids": data.get("payment_ids"),
            "partner_vat": data.get("partner_vat"),
            "pump_number": data.get("pump_number"),
            "employee_code": data.get("employee_code"),
            "suglaani_dugaar": data.get("suglaani_dugaar"),
            "total_amount": data.get("total_amount"),
            "sales_product_ids": data.get("sales_product_ids"),
            "ddtd": data.get("ddtd"),
            "noat_amount": data.get("noat_amount"),
        }

        request_data = json.dumps(data, cls=DjangoJSONEncoder)

        request_date = datetime.datetime.now()
        request_log = RequestLog.objects.create(
            terminal_id=str(self.terminal.pk),
            remote_address=self.remote_address,
            request_action='complete_trans',
            request_url="send_guur_txn",
            request_date=request_date,
            request_method=REQUEST_METHOD_POST,
            request_data=log_data,
            client_request_data=json.dumps(client_request_data, cls=DjangoJSONEncoder),
            operation_index=self.operation_index,
            created_date=request_date,
            last_updated_date=request_date
        )

        logger.info(
            'POS_SYNC_GUUR_TRANSACTION Terminal-ID: %r, Request-Actions: %r, Request-Date: %r, Request-Data: %r' % (
                self.terminal.terminal_pos_no,
                request_log.request_action,
                request_log.request_date,
                client_request_data
            )
        )

        try:
            response = session.post(
                self.guur_transaction_url,
                data=request_data,
                timeout=30,
                headers=headers
            )
        except requests.exceptions.RequestException as exception:
            send_discord_alert(
                channel_url=settings.DISCORD_RBP_ALERT_CHANNEL_URL,
                msg="GUUR CONNECTION FAIL. ACTION: %r, RBP: %s, TERMINAL: %r, EXC: %r" % (
                    "REMOTE_POS_COMPLETE_TRANSACTION",
                    "" if remote_backend_provider is None else remote_backend_provider.__unicode__(),
                    terminal.id_bank,
                    exception
                )
            )

            # logger.error(
            #     'REMOTE_POS_COMPLETE_TRANSACTION Terminal-ID: %r, Request-Actions: %r, RBP: %r, Exception: %r, Request-Date: %r, Request-Data: %r' % (
            #         terminal.id_bank,
            #         request_log.request_action,
            #         remote_backend_provider,
            #         request_log.exception,
            #         request_log.request_date,
            #         client_request_data
            #     )
            # )

            response_date = datetime.datetime.now()
            request_log.response_date = response_date
            request_log.response_data = None
            request_log.exception = str(exception)
            request_log.last_updated_date = response_date
            request_log.duration = str((response_date - request_date).total_seconds())
            request_log.save()

            return None, None, request_log

        if response.status_code != requests.codes.ok:
            response_date = datetime.datetime.now()
            request_log.response_date = response_date
            request_log.response_data = None
            request_log.response_code = str(response.status_code)
            request_log.last_updated_date = response_date
            request_log.duration = str((response_date - request_date).total_seconds())
            request_log.save()

            send_discord_alert(
                channel_url=settings.DISCORD_RBP_ALERT_CHANNEL_URL,
                msg="RBP REQUEST BAD STATUS FAIL. ACTION: %r, RBP: %s, TERMINAL: %r, STATUS CODE: %r" % (
                    "REMOTE_BACKEND_PROVIDER_COMPLETE_TRANSACTION",
                    "" if remote_backend_provider is None else remote_backend_provider.__unicode__(),
                    terminal.id_bank,
                    response.status_code
                )
            )

            return response.status_code, None, request_log

        response_data = response.json()

        # Mask
        response_data = response.json()
        log_response_data = copy.deepcopy(response_data)
        log_data = get_log_data(log_response_data, terminal)

        response_date = datetime.datetime.now()
        request_log.response_date = response_date
        request_log.response_data = log_data
        request_log.response_code = str(response.status_code)
        request_log.last_updated_date = response_date
        request_log.duration = str((response_date - request_date).total_seconds())
        request_log.response_status_code = response_data.get('status_code', 'ng')
        request_log.save()

        if payment is not None:
            # save remote payment
            TWO_PLACES = decimal.Decimal(10) ** -2
            amount = float(decimal.Decimal(transaction.get("total", "0")).quantize(TWO_PLACES))

            card_amount = 0
            cash_amount = 0
            other_amount = 0
            for payment_line in transaction.get("payment_lines", []):
                if payment_line.get("payment_service", "") == "CASH":
                    cash_amount += decimal.Decimal(payment_line.get("pay_amount", 0))
                elif payment_line.get("payment_service", "") == "CARD":
                    card_amount += decimal.Decimal(payment_line.get("pay_amount", 0))
                else:
                    other_amount += decimal.Decimal(payment_line.get("pay_amount", 0))

            payment = RemotePayment.objects.create(
                remote_backend_provider_id=str(remote_backend_provider.pk),
                remote_backend_provider_name=remote_backend_provider.name,
                terminal_id=str(terminal.pk),
                terminal_id_bank=str(terminal.id_bank),
                terminal_name=str(terminal.name),
                terminal_is_test=terminal.is_test,
                merchant_id=str(terminal.merchant.pk),
                merchant_name=str(terminal.merchant.name_format),
                action='sync_transaction',
                amount=decimal.Decimal(amount),
                card_amount=decimal.Decimal(card_amount),
                cash_amount=decimal.Decimal(cash_amount),
                other_amount=decimal.Decimal(other_amount),
                created_date=request_date
            )

        return response_data