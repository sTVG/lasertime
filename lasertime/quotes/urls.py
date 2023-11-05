from django.urls import path
from .views import quote_view

urlpatterns = [
    path('', quote_view, name='quote_view'),
]