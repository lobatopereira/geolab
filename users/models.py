from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from custom.models import Municipality
import uuid
from custom.utils_upload import upload_profile

import datetime


class Profile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)
	pob = models.CharField(max_length=50, verbose_name='Fatin Moris', null=True, blank=True)
	dob = models.DateField(verbose_name='Data Moris', null=True, blank=True)
	sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=6, null=True, blank=True)
	image = models.ImageField(upload_to=upload_profile, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','gif'])], verbose_name="Upload Imajen")
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def getAge(self):
		if self.dob:
			return datetime.date.today().year - self.dob.year
		else:
			return 0
			
	def getTotalLogin(self):
		return AuditLogin.objects.filter(user=self.user).count()
		
	def __str__(self):
		template = '{0.user}, {0.first_name} {0.last_name}'
		return template.format(self)


class AuditLogin(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="audituserlogin")
	login_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

		
	def __str__(self):
		template = '{0.user}, {0.login_time}'
		return template.format(self)

class AuditSystem(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	id_login = models.ForeignKey(User, on_delete=models.CASCADE)
	table = models.CharField(max_length=50, verbose_name='Tabela', null=True, blank=True)
	action = models.CharField(max_length=50, verbose_name='Asaun', null=True, blank=True)
	before = models.CharField(max_length=50, verbose_name='Dados Antes', null=True, blank=True)
	after = models.CharField(max_length=50, verbose_name='Dados Depois', null=True, blank=True)

		
	def __str__(self):
		template = '{0.action}, {0.table}'
		return template.format(self)


# pg_dump -U postgres -d db_laboratory -Fc -f C:\backup_file.dump

# pg_restore -U postgres -d db_laboratory -h localhost -p 5432 -W C:\backup_file.dump



