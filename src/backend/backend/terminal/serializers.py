from rest_framework import serializers

class TerminalSetSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    terminal_id = serializers.CharField(max_length=100, allow_blank=True, required=False)
    terminal_pos_no = serializers.CharField(max_length=100, allow_blank=True, required=True)

    mac_address = serializers.CharField(max_length=100, allow_blank=True, required=False)
    ip_address = serializers.CharField(max_length=100, allow_blank=True, required=False)

    guur_user = serializers.CharField(max_length=100, allow_blank=True, required=False)
    application_version = serializers.CharField(max_length=100, allow_blank=True, required=False)

    tbd_application_version = serializers.CharField(max_length=100, allow_blank=True, required=False)
    tdb_terminal_id = serializers.CharField(max_length=100, allow_blank=True, required=False)

    pts_ip_address = serializers.CharField(max_length=100, allow_blank=True, required=False)
