from django.urls import path
from .views import DataBaseMssqlView

urlpatterns = [
    path('database/', DataBaseMssqlView.as_view(), name='database_mssql')
]
