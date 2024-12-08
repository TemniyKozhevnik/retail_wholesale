from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.retail_analysis, name='retail_analysis'),
]