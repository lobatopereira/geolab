from django.contrib import admin
from equipments.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class KategoriaResource(resources.ModelResource):
    class Meta:
        model = Kategoria
class KategoriaAdmin(ImportExportModelAdmin):
    resource_class = KategoriaResource
admin.site.register(Kategoria, KategoriaAdmin)

class DoadoresResource(resources.ModelResource):
    class Meta:
        model = Doadores
class DoadoresAdmin(ImportExportModelAdmin):
    resource_class = DoadoresResource
admin.site.register(Doadores, DoadoresAdmin)

class EkipamentuResource(resources.ModelResource):
    class Meta:
        model = Ekipamentu
class EkipamentuAdmin(ImportExportModelAdmin):
    resource_class = EkipamentuResource
admin.site.register(Ekipamentu, EkipamentuAdmin)

class KuantidadeEkipamentuResource(resources.ModelResource):
    class Meta:
        model = KuantidadeEkipamentu
class KuantidadeEkipamentuAdmin(ImportExportModelAdmin):
    resource_class = KuantidadeEkipamentuResource
admin.site.register(KuantidadeEkipamentu, KuantidadeEkipamentuAdmin)

class DetalluEkipamentuResource(resources.ModelResource):
    class Meta:
        model = DetalluEkipamentu
class DetalluEkipamentuAdmin(ImportExportModelAdmin):
    resource_class = DetalluEkipamentuResource
admin.site.register(DetalluEkipamentu, DetalluEkipamentuAdmin)

class UtilizadorResource(resources.ModelResource):
    class Meta:
        model = Utilizador
class UtilizadorAdmin(ImportExportModelAdmin):
    resource_class = UtilizadorResource
admin.site.register(Utilizador, UtilizadorAdmin)

class UtilizaEkipamentuResource(resources.ModelResource):
    class Meta:
        model = UtilizaEkipamentu
        fields = '__all__'
        # def get_model_fields(self):
        #     return [field.name for field in self._meta.model._meta.fields]
class UtilizaEkipamentuAdmin(ImportExportModelAdmin):
    resource_class = UtilizaEkipamentuResource
    def get_list_display(self, request):
        # Dynamically generate list_display based on model fields
        model_fields = [field.name for field in UtilizaEkipamentu._meta.get_fields()]
        return model_fields
admin.site.register(UtilizaEkipamentu, UtilizaEkipamentuAdmin)

class LabInventoryResource(resources.ModelResource):
    class Meta:
        model = LabInventory
class LabInventoryAdmin(ImportExportModelAdmin):
    resource_class = LabInventoryResource
admin.site.register(LabInventory, LabInventoryAdmin)

class LabInventoryStockResource(resources.ModelResource):
    class Meta:
        model = LabInventoryStock
class LabInventoryStockAdmin(ImportExportModelAdmin):
    resource_class = LabInventoryStockResource
admin.site.register(LabInventoryStock, LabInventoryStockAdmin)

class LabInventoryTransactionResource(resources.ModelResource):
    class Meta:
        model = LabInventoryTransaction
class LabInventoryTransactionAdmin(ImportExportModelAdmin):
    resource_class = LabInventoryTransactionResource
admin.site.register(LabInventoryTransaction, LabInventoryTransactionAdmin)


# admin.site.register(Kategoria)
# admin.site.register(Doadores)
# admin.site.register(Ekipamentu)
# admin.site.register(KuantidadeEkipamentu)
# admin.site.register(DetalluEkipamentu)