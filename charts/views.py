from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from equipments.models import *
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from datetime import date
from reports.utils import getFulanNaran

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ADashCharts(request):
	group = request.user.groups.all()[0].name
	totalEkipamentu = DetalluEkipamentu.objects.all().count()
	totalInventory = LabInventory.objects.all().count()
	ekipamentuUzaHela = DetalluEkipamentu.objects.filter(status='Uza Hela').count()
	ekipamentuDisponivel = DetalluEkipamentu.objects.filter(status='Disponivel').count()
	ekipamentuDiak = DetalluEkipamentu.objects.filter(kondisaun='Diak').count()
	ekipamentuAat = DetalluEkipamentu.objects.filter(kondisaun='Aat').count()
	context ={
		"totalInventory":totalInventory,
		"totalEkipamentu":totalEkipamentu,
		"ekipamentuUzaHela":ekipamentuUzaHela,
		"ekipamentuDisponivel":ekipamentuDisponivel,
		"ekipamentuDiak":ekipamentuDiak,
		"ekipamentuAat":ekipamentuAat,
		"active_grafiku":"active",
		"title":f"Relatoriu ho formatu Grafiku",
	}
	return render(request, "charts_a/dash.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def chartStatusEkipamentu(request):
	group = request.user.groups.all()[0].name
	labels = []
	data = []
	ekipamentuUzaHela = DetalluEkipamentu.objects.filter(status='Uza Hela').count()
	ekipamentuDisponivel = DetalluEkipamentu.objects.filter(status='Disponivel').count()
	labels = ["Ekipamentu Uza Hela","Ekipamentu Disponivel"]
	data = [ekipamentuUzaHela,ekipamentuDisponivel]
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def chartKondisaunEkipamentu(request):
	group = request.user.groups.all()[0].name
	labels = []
	data = []
	ekipamentuDiak = DetalluEkipamentu.objects.filter(kondisaun='Diak').count()
	ekipamentuAat = DetalluEkipamentu.objects.filter(kondisaun='Aat').count()
	labels = ["Ekipamentu Diak","Ekipamentu Aar"]
	data = [ekipamentuDiak,ekipamentuAat]
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def chartEkipamentusupplytuirdoadornofulantianatual(request):
	group = request.user.groups.all()[0].name
	labels = []
	data = []
	ekipamentuDiak = DetalluEkipamentu.objects.filter(kondisaun='Diak').count()
	ekipamentuAat = DetalluEkipamentu.objects.filter(kondisaun='Aat').count()
	labels = ["Ekipamentu Diak","Ekipamentu Aar"]
	data = [ekipamentuDiak,ekipamentuAat]
	return JsonResponse(data={
		'labels':labels,
		'data':data,
		})