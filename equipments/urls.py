from django.urls import path
from . import views
urlpatterns = [

	##############
	path('dash/', views.EquipmentsDash, name="EquipmentsDash"),
	path('equipments/add/', views.createEquipment, name="createEquipment"),
	path('equipments/update/<str:hashid>', views.updateEquipment, name="updateEquipment"),
	path('equipments/detail/<str:hashid>', views.detailEquipment, name="detailEquipment"),
	path('equipments/quantity/set/<str:hashid>', views.createEquipmentQuantity, name="createEquipmentQuantity"),
	path('equipments/category/<str:hashid>', views.equipmentCategory, name="equipmentCategory"),
	

	# serverside link
	path('ekipamentu_data/', views.EkipamentuListJson.as_view(), name='ekipamentu_data'),
	path('ekipamentudataserverside/', views.EkipamentuListServerSide, name='EkipamentuListServerSide'),
	
	path('ekipamentu_data1/', views.EkipamentuListJson1.as_view(), name='ekipamentu_data1'),
	path('ekipamentudataserverside1/', views.EkipamentuListServerSide1, name='EkipamentuListServerSide1'),

	path('equipments/add/serial-number/<str:hashid>', views.createEquipmentDetail, name="createEquipmentDetail"),
	path('equipments/update/serial-number/<str:hashid>', views.updateEquipmentDetail, name="updateEquipmentDetail1"),
	
	# categoria
	path('category/dash/', views.EquipmentsCategoryDash, name="EquipmentsCategoryDash"),
	path('category/add/', views.createCategory, name="createCategory"),
	path('category/update/<str:hashid>', views.updateCategory, name="updateCategory"),
	path('category/delete/<str:hashid>', views.deleteCategory, name="deleteCategory"),
	
	# doador
	path('doador/dash/', views.DoadorDash, name="DoadorDash"),
	path('doador/add/', views.createDoador, name="createDoador"),
	path('doador/update/<str:hashid>', views.updateDoador, name="updateDoador"),
	path('doador/delete/<str:hashid>', views.deleteDoador, name="deleteDoador"),

	# utilizador
	path('utilizador/dash/', views.UtilizadorEquipmentuDash, name="UtilizadorEquipmentuDash"),
	path('detallu/ekipamentu/<str:hashid>/lista/historia/', views.DetailDetalluEquipment, name="DetailDetalluEquipment"),
	path('utilizador/add/', views.UtilizadorEquipmentuAdd, name="UtilizadorEquipmentuAdd"),
	path('utilizador/update/<str:hashid>', views.UtilizadorEquipmentuUpdate, name="UtilizadorEquipmentuUpdate"),
	path('utilizador/detail/<str:hashid>', views.UtilizadorEquipmentuDetail, name="UtilizadorEquipmentuDetail"),
	path('utilizador/detail/<str:hashid>/ekipamentu/uza/hela/', views.UtilizadorEquipmentuDetail, name="UtilizadorEquipmentuDetail1"),
	path('utilizador/detail/<str:hashid>/historia/utiliza/ekipamentu/', views.HistoriaUtilizaEquipmentu, name="HistoriaUtilizaEquipmentu"),
	
	# entrega
	path('utilizador/entrega/ekipamentu/dash/', views.UtilizadorEntregaEquipmentuDash, name="UtilizadorEntregaEquipmentuDash"),
	path('utilizador/entrega/ekipamentu/<str:hashid>', views.EntregaEkipamentu, name="EntregaEkipamentu"),

	# uza ekipamentu
	path('utilizador/uza/ekipamentu/dash/', views.UtilizadorUzaEquipmentuDash, name="UtilizadorUzaEquipmentuDash"),
	path('utilizador/uza/ekipamentu/empresta/<str:hashid>', views.UtilizadorUzaEquipmentuEmpresta, name="UtilizadorUzaEquipmentuEmpresta"),
	path('utilizador/<str:hashid>/empresta/ekipamentu/multi/', views.UtilizadorEmprestaEquipmentu, name="UtilizadorEmprestaEquipmentu"),
	path('historia/empresta/utiliza/ekipamentu/laboratoriu/', views.HistoriaUtilazaEkipamentuLaboratoriu, name="HistoriaUtilazaEkipamentuLaboratoriu"),
	

	# inventory
	path('inventory/dash/', views.InventoryDash, name="InventoryDash"),
	path('inventory/add/', views.createInventory, name="createInventory"),
	path('inventory/category/<str:hashid>', views.inventoryCategory, name="inventoryCategory"),
	path('inventory/update/<str:hashid>', views.updateInventory, name="updateInventory"),
	path('inventory/detail/<str:hashid>', views.detailInventory, name="detailInventory"),
	path('inventory/detail/<str:hashid>/quantity/in/', views.registerInventoryKuantityIn, name="registerInventoryKuantityIn"),
	# uza inventaria
	path('inventory/uza/dash/', views.InventoryUzaDash, name="InventoryUzaDash"),
	path('inventory/<str:hashid>/uza/register/', views.UzaInventory, name="UzaInventory"),
	
	path('utilizador/detail/<str:hashid>/historia/utiliza/inventaria/', views.HistoriaUtilizaInventory, name="HistoriaUtilizaInventory"),

	# notif
	path('notifikasaun/utilizador/uza/liu-loron-atu-entrega/', views.notifUsedDeadlineList, name="notifUsedDeadlineList"),
	path('notifikasaun/utilizador/uza/deadline-loron-iha-aban/', views.notifUsedDeadlineAbanList, name="notifUsedDeadlineAbanList"),


]