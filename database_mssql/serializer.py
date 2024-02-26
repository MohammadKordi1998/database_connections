from rest_framework import serializers


class DataBaseConnectionMssqlSerializer(serializers.Serializer):
    server = serializers.RegexField(
        regex=r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
    )
    port = serializers.RegexField(
        regex=r'^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'
    )
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
