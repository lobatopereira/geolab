import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import Municipality
from users.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.urls import reverse_lazy
from equipments.models import *
from custom.utils import *



@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def EquipmentsCategoryDash(request):
	group = request.user.groups.all()[0].name
	objects = Kategoria.objects.all()
	context = {
		'group': group, 
		'objects': objects,
		'page': "list",
		'active_kategoria':'active',
		'title': 'Kategoria Ekipamentu Laboratoriu', 'legend': 'Kategoria Ekipamentu Laboratoriu',
	}
	return render(request, 'category/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def createCategory(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid = getjustnewid(Kategoria)
		new_hashid = hash_md5(str(newid))
		category = request.POST.get("category")
		obj3 = Kategoria.objects.create(id=newid,kategoria=category,hashed=new_hashid,user_created=request.user)
		messages.success(request, f'Dadus Kategoria Ekipamentu Rejistu ho Susesu!')
		return redirect('EquipmentsCategoryDash')
	context = {
		'active_kategoria':'active',
		'title': 'Kategoria Ekipamentu Laboratoriu', 'legend': 'Kategoria Ekipamentu Laboratoriu',
	}
	return render(request, 'category/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def updateCategory(request,hashid):
	group = request.user.groups.all()[0].name
	objects = Kategoria.objects.get(hashed=hashid)
	if request.method == 'POST':
		category = request.POST.get("category")
		objects.kategoria = category
		objects.save()
		messages.success(request, f'Dadus Kategoria Ekipamentu Altera ho Susesu!')
		return redirect('EquipmentsCategoryDash')
	context = {
		'active_kategoria':'active',
		'title': 'Kategoria Ekipamentu Laboratoriu', 'legend': 'Kategoria Ekipamentu Laboratoriu',
	}
	return render(request, 'category/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def deleteCategory(request,hashid):
	group = request.user.groups.all()[0].name
	objects = Kategoria.objects.get(hashed=hashid)
	objects.delete()
	messages.success(request, f'Dadus Kategoria {objects.kategoria} Delete ho Susesu!')
	return redirect('EquipmentsCategoryDash')
	