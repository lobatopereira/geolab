from django.urls import path
from . import views
urlpatterns = [
	path('dash/', views.ReportDash, name="ReportDash"),
	path('dash/all-equipments/', views.reportAllEquipments, name="reportAllEquipments"),
	path('list/equipments/in-use/', views.reportEkipamentuUza, name="reportEkipamentuUza"),
	path('list/equipments/available/', views.reportEkipamentuDisponivel, name="reportEkipamentuDisponivel"),
	path('list/equipments/kondisaun-diak/', views.reportEkipamentuDiak, name="reportEkipamentuDiak"),
	path('list/equipments/kondisaun-aat/', views.reportEkipamentuAat, name="reportEkipamentuAat"),
	path('list/equipments/kategoria/<str:hashid>', views.ReportKategoriaEkipamentu, name="ReportKategoriaEkipamentu"),
	path('list/equipments/doador/<str:hashid>', views.ReportDoadorEkipamentu, name="ReportDoadorEkipamentu"),
	path('list/equipments/fulan/<str:idFulan>/doador/<str:doadorID>/', views.ReportDoadorEkipamentuTuirFulan, name="ReportDoadorEkipamentuTuirFulan"),
	path('list/equipments/tinan/<str:year>', views.ReportEkipamentuTuirTinan, name="ReportEkipamentuTuirTinan"),
	##############
	path('dash/all-inventaria/', views.reportAllInventaria, name="reportAllInventaria"),
	path('list/inventaria/kategoria/<str:hashid>', views.ReportKategoriaInventaria, name="ReportKategoriaInventaria"),
	path('list/inventaria/doador/<str:hashid>', views.ReportDoadorInventaria, name="ReportDoadorInventaria"),
	path('list/inventaria/tama/fulan/<str:idFulan>', views.ReportInventariaTamaTuirFulan, name="ReportInventariaTamaTuirFulan"),
	path('list/inventaria/sai/fulan/<str:idFulan>', views.ReportInventariaSaiTuirFulan, name="ReportInventariaSaiTuirFulan"),
	path('list/inventaria/tama/tinan/<str:year>', views.ReportInventariaTamaTuirTinan, name="ReportInventariaTamaTuirTinan"),
	path('list/inventaria/sai/tinan/<str:year>', views.ReportInventariaSaiTuirTinan, name="ReportInventariaSaiTuirTinan"),
	
]