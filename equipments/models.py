from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Kategoria(models.Model):
	kategoria = models.CharField(max_length=255, null=True)
	
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def totalekipamentu(self):
		return Ekipamentu.objects.filter(kategoria=self).count()

	def totalinventory(self):
		return LabInventory.objects.filter(kategoria=self).count()

	def __str__(self):
		template = '{0.kategoria}'
		return template.format(self)

class Doadores(models.Model):
	kodigu = models.CharField(max_length=255, null=True)
	doador = models.CharField(max_length=255, null=True)
	
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def __str__(self):
		template = '{0.doador}'
		return template.format(self)

class Ekipamentu(models.Model):
	kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE, null=True,related_name="katekipamentu")
	doador = models.ForeignKey(Doadores, on_delete=models.CASCADE, null=True,related_name="doadorekipamentu")
	data_simu = models.DateField(null=True,blank=True) 
	naran = models.CharField(max_length=255,null=True)
	marka = models.CharField(max_length=255,null=True)
	
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def kuantidade(self):
		kuantidade = KuantidadeEkipamentu.objects.filter(ekipamentu=self).last()
		if kuantidade:
			return kuantidade.kuantidade_inisiu
		else:
			return 0

	def __str__(self):
		template = '{0.naran}'
		return template.format(self)

class KuantidadeEkipamentu(models.Model):
	ekipamentu = models.OneToOneField(Ekipamentu, on_delete=models.CASCADE, null=True,related_name="kuantekipamentu")
	kuantidade_inisiu = models.IntegerField(blank=True, null=True,verbose_name="Kuantidade Inisiu")
	kuantidade_disponivel = models.IntegerField(blank=True, null=True,verbose_name="Kuantidade Disponivel")
	kuantidade_empresta = models.IntegerField(blank=True, null=True,verbose_name="Kuantidade Uza Hela")

	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def __str__(self):
		template = '{0.ekipamentu.naran} | {0.kuantidade_inisiu} | {0.kuantidade_disponivel}'
		return template.format(self)

class DetalluEkipamentu(models.Model):
	ekipamentu = models.ForeignKey(Ekipamentu, on_delete=models.CASCADE, null=True,related_name="detekipamentu")
	nu_serial = models.CharField(max_length=100,null=True)
	kondisaun = models.CharField(choices=[('Diak','Diak'),('Aat','Aat')], max_length=10, null=True, verbose_name="Kondisaun")
	status = models.CharField(choices=[('Uza Hela','Uza Hela'),('Disponivel','Disponivel')], max_length=30, null=True, verbose_name="Status Ekipamentu")
	image = models.ImageField(upload_to='DetalluEkipamentu', null=True,blank=True)

	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def dadusuza(self):
		objects = UtilizaEkipamentu.objects.filter(item=self).last()
		if objects:
			return objects
		else:
			return None

	def __str__(self):
		template = '{0.ekipamentu.naran} | {0.nu_serial} | {0.kondisaun} | {0.status}'
		return template.format(self)

class Utilizador(models.Model):
	naran = models.CharField(max_length=255,null=True, verbose_name="Naran Responsavel")
	pozisaun = models.CharField(max_length=255,null=True, verbose_name="Pozisaun")
	seksu = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=10, null=True, verbose_name="Seksu")
	nu_kontaktu = models.CharField(max_length=50,null=True,verbose_name="Nu. Kontaktu") 
	image = models.ImageField(upload_to='Utilizador', null=True,blank=True)

	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.naran}'
		return template.format(self)

class UtilizaEkipamentu(models.Model):
	ekipamentu = models.ForeignKey(Ekipamentu, on_delete=models.CASCADE, null=True,related_name="uzaekipamentu")
	item = models.ForeignKey(DetalluEkipamentu, on_delete=models.CASCADE, null=True,related_name="uzaekipamentu",verbose_name='Detallu Ekipamentu')
	utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, null=True,related_name="utilizadorekipamentu")
	data_empresta = models.DateField(null=True,blank=True,verbose_name="Data Empresta") 
	data_atu_entrega = models.DateField(null=True,blank=True,verbose_name="Data atu entrega")
	data_entrega = models.DateField(null=True,blank=True,verbose_name="Data entrega")
	total_loron_atu_uza = models.IntegerField(blank=True, null=True,verbose_name="Total Loron")
	total_loron_kontra = models.IntegerField(blank=True, null=True,verbose_name="Total Loron Kontra")
	is_return = models.BooleanField(default=False, null=True) 
	kondisaun = models.CharField(choices=[('Diak','Diak'),('Aat','Aat')], max_length=10,blank=True, null=True, verbose_name="Kondisaun Depois Uza")

	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def loron_kontra(self):
		today = timezone.now().date()
		total_days = (today - self.data_atu_entrega).days
		return total_days

	def __str__(self):
		template = '{0.data_empresta} '
		return template.format(self)

class LabInventory(models.Model):
	kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE, null=True,related_name="katinventory")
	doador = models.ForeignKey(Doadores, on_delete=models.CASCADE, null=True,related_name="doadorinventory")
	naran = models.CharField(max_length=255,null=True)
	dataTama = models.DateField(null=True,blank=True) 
	marka = models.CharField(max_length=255,null=True)
	image = models.ImageField(upload_to='LabInventory', null=True,blank=True)
	
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	# def kuantidade(self):
	# 	kuantidade = KuantidadeEkipamentu.objects.filter(ekipamentu=self).last()
	# 	if kuantidade:
	# 		return kuantidade.kuantidade_inisiu
	# 	else:
	# 		return 0

	def __str__(self):
		template = '{0.naran}'
		return template.format(self)

class LabInventoryStock(models.Model):
	inventory = models.OneToOneField(LabInventory,on_delete=models.CASCADE,null=True,related_name='inventoryStock')
	kodigu_stock = models.CharField(max_length=100,null=True,blank=True)
	total_tama = models.IntegerField(blank=True, null=True,verbose_name="Total Tama")
	total_stock = models.IntegerField(blank=True, null=True,verbose_name="Total Stock")
	total_sai = models.IntegerField(blank=True, null=True,verbose_name="Total Sai")

	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def __str__(self):
		template = '{0.inventory.naran}, {0.kodigu_stock}'
		return template.format(self)

class LabInventoryTransaction(models.Model):
	inventory = models.ForeignKey(LabInventory,on_delete=models.CASCADE,null=True,related_name='inventoryTransaction')
	utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, null=True,blank=True,related_name="utilizadorinventaria")
	data = models.DateField(null=True)
	total_tama = models.IntegerField(blank=True, null=True,verbose_name="Total Tama")
	total_sai = models.IntegerField(blank=True, null=True,verbose_name="Total Sai")
	total = models.IntegerField(blank=True, null=True,verbose_name="Total")
	is_confirm = models.BooleanField(default=False, null=True)
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def __str__(self):
		template = '{0.inventory.naran}, {0.data}, {0.total}'
		return template.format(self)
