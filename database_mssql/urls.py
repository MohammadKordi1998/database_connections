from django.urls import path
from .views import MssqlFindDatabaseView, MssqlFindTableView, MssqlFindColumnView

urlpatterns = [
    path('database/', MssqlFindDatabaseView.as_view(), name='mssql_find_database'),
    path('table/', MssqlFindTableView.as_view(), name='mssql_find_table'),
    path('column/', MssqlFindColumnView.as_view(), name='mssql_find_table'),
]
