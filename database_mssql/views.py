import pyodbc
import pandas as pd
from rest_framework import status
from utils.messaga import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import DataBaseConnectionMssqlSerializer


class DataBaseMssqlView(APIView):
    def post(self, request):
        try:
            serializer = DataBaseConnectionMssqlSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            server = serializer.validated_data.get('server')
            port = serializer.validated_data.get('port')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                connection = pyodbc.connect(
                    f'DRIVER={{SQL Server}}; SERVER={server}; PORT={port}; UID={username}; PWD={password}')
            except:
                message = Message(
                    text_message='Connection Failed',
                    status=False
                ).result_message()
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            query = '''SELECT database_id, name FROM sys.databases'''
            connection_result = pd.read_sql_query(query, connection)

            message = Message(
                text_message=connection_result.to_dict('records'),
                status=True
            ).result_message()
            return Response(message, status=status.HTTP_200_OK)

        except Exception as exc:
            message = Message(
                text_message=exc.args,
                status=False
            ).result_message()
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
