from . import views
from .views import *
from django.urls import path

app_name = 'number_work'
urlpatterns = [
    path('num_ident/', views.number_identification, name='num_ident'),
]
