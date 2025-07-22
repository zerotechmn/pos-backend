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
    taxType = serializers.CharField(max_length=100, )
    merchantTin = serializers.CharField(max_length=100, allow_null=True, required=False)
    customerTin = serializers.CharField(max_length=100, allow_null=True, required=False)
    totalVAT = serializers.FloatField()
    totalCityTax = serializers.FloatField()
    bankAccountNo = serializers.CharField(max_length=100, allow_blank=True, required=False)
    iBan = serializers.CharField(max_length=100, allow_blank=True, required=False)
    items = ItemSerializer(many=True)

class PaymentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100, )
    status = serializers.CharField(max_length=100, )
    paidAmount = serializers.FloatField()

class eBarimtReceiptSerializer(serializers.Serializer):
    regno = serializers.CharField(max_length=100)
    salesNo = serializers.CharField(max_length=100)
    totalAmount = serializers.FloatField()
    totalVAT = serializers.FloatField()
    totalCityTax = serializers.FloatField()
    districtCode = serializers.CharField(max_length=100, )
    merchantTin = serializers.CharField(max_length=100, )
    posNo = serializers.CharField(max_length=100, )
    customerTin = serializers.CharField(max_length=100, allow_null=True, required=False)
    consumerNo = serializers.CharField(max_length=100, required=False)
    type = serializers.CharField(max_length=100, )
    # inactiveId = serializers.CharField(max_length=100, allow_null=True)
    # invoiceId = serializers.CharField(max_length=100, allow_null=True)
    # billIdSuffix = serializers.CharField(max_length=100, )
    receipts = ReceiptSerializer(many=True)
    payments = PaymentSerializer(many=True)
