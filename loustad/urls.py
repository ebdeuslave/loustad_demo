from django.urls import path
from .views import ask

app_name = 'v'


urlpatterns = [
    path('', ask, name='ask' ),
    ]