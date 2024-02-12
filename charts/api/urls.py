from django.urls import path
from . import views

urlpatterns = [
    path('g/equipments/status/summary/', views.APIGEquipmentStatusSumm.as_view(), name="api-g-equipment-status-summary"),
    path('g/equipments/condition/summary/', views.APIGEquipmentKondisaunSumm.as_view(), name="api-g-equipment-condition-summary"),
    path('g/equipments/tama/tuir/fulan/tinan/atual/summary/', views.APIGEquipmentTamaFulanTinanAtual.as_view(), name="APIGEquipmentTamaFulanTinanAtual"),
    path('g/equipments/tama/tuir/tinan/', views.APIGEquipmentTamaTuirTinan.as_view(), name="APIGEquipmentTamaTuirTinan"),
    
    path('g/sumariu/ekipamentu/inventaria/tuir/kategoria/', views.APIGSummKategoria.as_view(), name="APIGSummKategoria"),
    path('g/sumariu/ekipamentu/inventaria/tuir/doador/', views.APIGSummDoador.as_view(), name="APIGSummDoador"),

    path('g/inventaria/tuir/fulan/tinan/atual/summary/', views.APIGInventariatuirFulanTinanAtual.as_view(), name="APIGInventariatuirFulanTinanAtual"),
    path('g/inventaria/tuir/tinan/summary/', views.APIGInventariaTuirTinan.as_view(), name="APIGInventariaTuirTinan"),
 
]