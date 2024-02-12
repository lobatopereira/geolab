from django.urls import path
from . import views

urlpatterns = [
    path('a/dashboard', views.ADashCharts, name="a-charts-dash"),

    path('a/chart/status/ekipamentu', views.chartStatusEkipamentu, name="a-charts-status-ekipamentu"),
    path('a/chart/kondisaun/ekipamentu', views.chartKondisaunEkipamentu, name="a-charts-kondisaun-ekipamentu"),


 
]