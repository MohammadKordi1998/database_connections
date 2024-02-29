import pandas as pd
from rest_framework import status
from utils.messaga import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.mssql.test_connection import TestConnection
from .serializer import MssqlFindDataBaseSerializer, MssqlFindTableSerializer, MssqlFindFieldsSerializer


class MssqlFindDatabaseView(APIView):
    def post(self, request):
        try:
            serializer = MssqlFindDataBaseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            server = serializer.validated_data.get('server')
            port = serializer.validated_data.get('port')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            connection = TestConnection(
                server=server,
                port=port,
                username=username,
                password=password,
                database_name=None
            ).connect()

            if connection['status']:
                connection = connection['message']
            else:
                return Response(connection, status=status.HTTP_400_BAD_REQUEST)

            query = '''SELECT database_id, name FROM sys.databases;'''
            connection_result = pd.read_sql_query(query, connection)

            message = Message(
                message=connection_result.to_dict('records'),
                status=True
            ).result_message()
            return Response(message, status=status.HTTP_200_OK)

        except Exception as exc:
            message = Message(
                message=exc.args,
                status=False
            ).result_message()
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class MssqlFindTableView(APIView):
    def post(self, request):
        try:
            serializer = MssqlFindTableSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            server = serializer.validated_data.get('server')
            port = serializer.validated_data.get('port')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            database_name = serializer.validated_data.get('database')

            connection = TestConnection(
                server=server,
                port=port,
                username=username,
                password=password,
                database_name=database_name
            ).connect()

            if connection['status']:
                connection = connection['message']
            else:
                return Response(connection, status=status.HTTP_400_BAD_REQUEST)

            query = '''SELECT * FROM information_schema.tables;'''
            connection_result = pd.read_sql_query(query, connection)

            message = Message(
                message=connection_result.to_dict('records'),
                status=True
            ).result_message()
            return Response(message, status=status.HTTP_200_OK)

        except Exception as exc:
            message = Message(
                message=exc.args,
                status=False
            ).result_message()
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class MssqlFindColumnView(APIView):
    def post(self, request):
        try:
            serializer = MssqlFindFieldsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            server = serializer.validated_data.get('server')
            port = serializer.validated_data.get('port')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            database_name = serializer.validated_data.get('database')
            table_name = serializer.validated_data.get('table')

            connection = TestConnection(
                server=server,
                port=port,
                username=username,
                password=password,
                database_name=database_name
            ).connect()

            if connection['status']:
                connection = connection['message']
            else:
                return Response(connection, status=status.HTTP_400_BAD_REQUEST)

            query = f'''SELECT * FROM {table_name};'''
            query_type = f"""SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}';"""
            type_data = pd.read_sql_query(query_type, connection)
            data = pd.read_sql_query(query, connection)
            data = data.fillna('')

            for key in type_data.values:
                key[1] = key[1].replace('null', 'None')
                key[1] = key[1].replace('bit', 'bool')
                key[1] = key[1].replace('bigint', 'int')
                key[1] = key[1].replace('bit', 'int')
                key[1] = key[1].replace('float', 'float')
                key[1] = key[1].replace('numeric', 'decimal.Decimal')
                key[1] = key[1].replace('varchar', 'str')
                key[1] = key[1].replace('nstr', 'str')
                key[1] = key[1].replace('nvarchar', 'str')
                key[1] = key[1].replace('varbinary', 'bytes')
                key[1] = key[1].replace('date', 'datetime.date')
                key[1] = key[1].replace('time', 'datetime.time')
                key[1] = key[1].replace('datetime', 'datetime.datetime')
                key[1] = key[1].replace('uniqueidentifier', 'uuid.UUID')

            message = Message(
                message=dict(
                    data=data.to_dict('records'),
                    type=type_data.to_dict('records')
                ),
                status=True
            ).result_message()
            return Response(message, status=status.HTTP_200_OK)

        except Exception as exc:
            message = Message(
                message=exc.args,
                status=False
            ).result_message()
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
