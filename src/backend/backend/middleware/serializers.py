from rest_framework import serializers

class GuurAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

class GuurBaseSerializer(serializers.Serializer):
    shts_code = serializers.CharField(max_length=100, required=True)


class GuurProductSerializer(serializers.Serializer):
    shts_code = serializers.CharField(max_length=100, required=True)

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    barCode = serializers.CharField(max_length=100)
    barCodeType = serializers.CharField(max_length=100)
    classificationCode = serializers.CharField(max_length=100)
    taxProductCode = serializers.CharField(allow_null=True, required=False)
    measureUnit = serializers.CharField(max_length=100)
    qty = serializers.FloatField()
    unitPrice = serializers.FloatField()
    totalVAT = serializers.FloatField()
    totalCityTax = serializers.FloatField()
    totalAmount = serializers.FloatField()
    totalBonus = serializers.FloatField()

class ReceiptSerializer(serializers.Serializer):
    totalAmount = serializers.FloatField()
    taxType = serializers.CharField(max_length=100)
    merchantTin = serializers.CharField(max_length=100, allow_null=True, required=False)
    customerTin = serializers.CharField(max_length=100, allow_null=True, required=False)
    totalVAT = serializers.FloatField()
    totalCityTax = serializers.FloatField()
    bankAccountNo = serializers.CharField(max_length=100, allow_blank=True, required=False)
    iBan = serializers.CharField(max_length=100, allow_blank=True, required=False)
    items = ItemSerializer(many=True)

class PaymentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=100)
    paidAmount = serializers.FloatField()

class eBarimtReceiptSerializer(serializers.Serializer):
    regno = serializers.CharField(max_length=100)
    salesNo = serializers.CharField(max_length=100)
    totalAmount = serializers.FloatField()
    totalVAT = serializers.FloatField()
    totalCityTax = serializers.FloatField()
    districtCode = serializers.CharField(max_length=100)
    merchantTin = serializers.CharField(max_length=100)
    posNo = serializers.CharField(max_length=100)
    customerTin = serializers.CharField(max_length=100, allow_null=True, required=False)
    consumerNo = serializers.CharField(max_length=100, required=False)
    type = serializers.CharField(max_length=100)
    # inactiveId = serializers.CharField(max_length=100, allow_null=True)
    # invoiceId = serializers.CharField(max_length=100, allow_null=True)
    # billIdSuffix = serializers.CharField(max_length=100)
    receipts = ReceiptSerializer(many=True)
    payments = PaymentSerializer(many=True)

class PaymentIdsItemSerializer(serializers.Serializer):
    sale_id = serializers.IntegerField()
    transaction_date = serializers.CharField(max_length=100, allow_blank=True, required=False)
    amount_paid = serializers.FloatField()
    payment_type = serializers.CharField(max_length=100, allow_blank=True, required=False)
    total_amount = serializers.FloatField()
    card_maskal = serializers.CharField(max_length=100, allow_blank=True, required=False)
    car_number = serializers.CharField(max_length=100, allow_blank=True, required=False)
    discount = serializers.FloatField()
    talon_serial_number = serializers.CharField(max_length=100, allow_blank=True, required=False)
    partner_vat = serializers.CharField(max_length=100, allow_blank=True, required=False)
    trace_no = serializers.CharField(max_length=100, allow_blank=True, required=False)

class SalesProductIdsItemSerializer(serializers.Serializer):
    sale_id = serializers.IntegerField()
    code = serializers.CharField(max_length=100, allow_blank=True, required=False)
    size = serializers.FloatField()
    total_amount = serializers.FloatField()
    product_id = serializers.IntegerField()
    vat = serializers.BooleanField()
    unit_price = serializers.FloatField()
    barcode = serializers.CharField(max_length=100, allow_blank=True, required=False)

class GuurTransactionSerializer():
    source = serializers.CharField(max_length=100, allow_blank=True, required=False)
    comport = serializers.IntegerField()
    pay_amount = serializers.FloatField()
    discount = serializers.FloatField()
    pos_number = serializers.CharField(max_length=100, allow_blank=True, required=False)
    shts_code = serializers.CharField(max_length=100, allow_blank=True, required=False)
    payment_ids = PaymentIdsItemSerializer(many=True)
    partner_vat = serializers.CharField(max_length=100, allow_blank=True, required=False)
    pump_number = serializers.IntegerField()
    employee_code = serializers.CharField(max_length=100, allow_blank=True, required=False)
    suglaani_dugaar = serializers.CharField(max_length=100, allow_blank=True, required=False)
    total_amount = serializers.FloatField()
    hoshuu = serializers.IntegerField()
    sales_product_ids = SalesProductIdsItemSerializer(many=True)
    ddtd = serializers.CharField(max_length=100, allow_blank=True, required=False)
    noat_amount = serializers.FloatField()


# LML Serializers
class LMSAuthTokenSerializer(serializers.Serializer):
    posCode = serializers.CharField(max_length=100, allow_blank=True, required=True)
    branchCode = serializers.CharField(max_length=100, allow_blank=True, required=True)
    merchantTtd = serializers.CharField(max_length=100, allow_blank=True, required=False)
    name = serializers.CharField(max_length=100, allow_blank=True, required=False)
