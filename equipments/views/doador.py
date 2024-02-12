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
def DoadorDash(request):
	group = request.user.groups.all()[0].name
	objects = Doadores.objects.all()
	context = {
		'objects': objects,'group': group,
		'page': "list",'active_doador':'active',
		'title': 'Dadus Doadores', 'legend': 'Dadus Doadores',
	}
	return render(request, 'doador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def createDoador(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid = getjustnewid(Doadores)
		new_hashid = hash_md5(str(newid))
		doador = request.POST.get("doador")
		kodigu = request.POST.get("kodigu")
		obj3 = Doadores.objects.create(id=newid,doador=doador,kodigu=kodigu,hashed=new_hashid,user_created=request.user)
		messages.success(request, f'Dadus Doador Ekipamentu Rejistu ho Susesu!')
		return redirect('DoadorDash')
	context = {
		'active_doador':'active',
		'title': 'Doador Ekipamentu Laboratoriu', 'legend': 'Doador Ekipamentu Laboratoriu',
	}
	return render(request, 'doador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def updateDoador(request,hashid):
	group = request.user.groups.all()[0].name
	objects = Doadores.objects.get(hashed=hashid)
	if request.method == 'POST':
		doador = request.POST.get("doador")
		objects.doador = doador
		kodigu = request.POST.get("kodigu")
		objects.kodigu = kodigu
		objects.save()
		messages.success(request, f'Dadus Doador Altera ho Susesu!')
		return redirect('DoadorDash')
	context = {
		'active_doador':'active',
		'title': 'Doador Ekipamentu Laboratoriu', 'legend': 'Doador Ekipamentu Laboratoriu',
	}
	return render(request, 'doador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def deleteDoador(request,hashid):
	group = request.user.groups.all()[0].name
	objects = Doadores.objects.get(hashed=hashid)
	objects.delete()
	messages.error(request, f'Dadus Doador {objects.doador} Delete ho Susesu!')
	return redirect('DoadorDash')
	