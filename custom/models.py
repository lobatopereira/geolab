from django.db import models
import uuid

class Country(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=5, null=True)
	name = models.CharField(max_length=50, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Municipality(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=5, null=True)
	name = models.CharField(max_length=50, verbose_name="Naran")
	hckey = models.CharField(max_length=10, null=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}, {0.municipality.name}'
		return template.format(self)

class Village(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AcademicLevel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Profession(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)


