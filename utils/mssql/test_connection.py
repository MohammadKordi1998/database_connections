import pyodbc

from utils.messaga import Message


class TestConnection:
    def __init__(self, server, port, username, password, database_name=None):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name

    def connect(self):
        try:
            if self.database_name:
                connection = pyodbc.connect(
                    f'DRIVER={{SQL Server}}; SERVER={self.server}; PORT={self.port}; UID={self.username}; PWD={self.password}; DATABASE={self.database_name}'
                )
            else:
                connection = pyodbc.connect(
                    f'DRIVER={{SQL Server}}; SERVER={self.server}; PORT={self.port}; UID={self.username}; PWD={self.password}'
                )
            message = Message(
                message=connection,
                status=True
            ).result_message()
            return message
        except:
            message = Message(
                message='Connection Failed',
                status=False
            ).result_message()
            return message
