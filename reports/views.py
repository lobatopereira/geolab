from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from users.models import Profile
from equipments.models import *
from django.db.models import Count, Q
from django.db.models import Sum
from django.contrib.auth.models import User, Group
from datetime import date
from reports.utils import getFulanNaran,getFulanNumeru

# Create your views here.

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportDash(request):
	group = request.user.groups.all()[0].name
	totalEkipamentu = DetalluEkipamentu.objects.all().count()
	totalInventory = LabInventory.objects.all().count()
	ekipamentuUzaHela = DetalluEkipamentu.objects.filter(status='Uza Hela').count()
	ekipamentuDisponivel = DetalluEkipamentu.objects.filter(status='Disponivel').count()
	ekipamentuDiak = DetalluEkipamentu.objects.filter(kondisaun='Diak').count()
	ekipamentuAat = DetalluEkipamentu.objects.filter(kondisaun='Aat').count()
	listaDoador = Doadores.objects.all()
	monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
	sumariu_tuir_fulan_tinan_atual = []
	for x in monthListOrder:
		sumariuTuirFulan = []
		for i in listaDoador:
			totalEkipamentuDoador = DetalluEkipamentu.objects.filter(ekipamentu__doador__id=i.id,ekipamentu__data_simu__month=x,ekipamentu__data_simu__year=date.today().year).count()
			sumariuTuirFulan.append({"doador":i.kodigu,"doadorID":i.hashed,"totalEkipamentu":totalEkipamentuDoador})
		sumariu_tuir_fulan_tinan_atual.append({
			"fulan":getFulanNaran(x),
			"idFulan":x,
			"sumariuTuirFulan":sumariuTuirFulan,
			})


	years = DetalluEkipamentu.objects.distinct().values('ekipamentu__data_simu__year').all().order_by('ekipamentu__data_simu__year')
	sumario_kada_tinan = []
	for x in years:
		totalEkipamentuTinan = DetalluEkipamentu.objects.filter(ekipamentu__data_simu__year=x['ekipamentu__data_simu__year']).count()
		sumario_kada_tinan.append({
			"year":x['ekipamentu__data_simu__year'],
			"totalEkipamentu":totalEkipamentuTinan,
			})	

	years = LabInventoryTransaction.objects.distinct().values('data__year').all().order_by('data__year')
	sumario_inventaria_kada_tinan = []
	for x in years:
		totaltama = LabInventoryTransaction.objects.filter(data__year=x['data__year']).aggregate(total_sum=Sum('total_tama'))['total_sum']
		if totaltama:
			totaltama = totaltama
		else:
			totaltama = 0
		totalsai = LabInventoryTransaction.objects.filter(data__year=x['data__year']).aggregate(total_sum=Sum('total_sai'))['total_sum']
		if totalsai:
			totalsai = totalsai
		else:
			totalsai = 0
		sumario_inventaria_kada_tinan.append({
			"year":x['data__year'],
			"tama":totaltama,
			"sai":totalsai,
			})	

	sumariu_inventaria_tuir_fulan_tinan_atual = []
	for x in monthListOrder:
		totaltama = LabInventoryTransaction.objects.filter(data__month=x,data__year=date.today().year).aggregate(total_sum=Sum('total_tama'))['total_sum']
		if totaltama:
			totaltama = totaltama
		else:
			totaltama = 0
		totalsai = LabInventoryTransaction.objects.filter(data__month=x,data__year=date.today().year).aggregate(total_sum=Sum('total_sai'))['total_sum']
		if totalsai:
			totalsai = totalsai
		else:
			totalsai = 0

		sumariu_inventaria_tuir_fulan_tinan_atual.append({
			"fulan":getFulanNaran(x),
			"idFulan":x,
			"tama":totaltama,
			"sai":totalsai,
			})
	
	sumario_doador = []
	listaDoador = Doadores.objects.all()
	for x in listaDoador:
		obj1 = DetalluEkipamentu.objects.filter(ekipamentu__doador__id=x.id).count()
		obj2 = LabInventoryStock.objects.filter(inventory__doador__id=x.id).aggregate(total_sum=Sum('total_stock'))['total_sum']
		if obj2:
			obj2 = obj2
		else:
			obj2 = 0
		if x.kodigu:
			doador = x.kodigu
		else:
			doador = x.doador
		sumario_doador.append({
			"id_doador":x.hashed,
			"doador":doador,
			"totalEkipamentu":obj1,
			"totalInventaria":obj2
			})
	sumario_kategoria = []
	listaKategoria = Kategoria.objects.all()
	for x in listaKategoria:
		obj1 = DetalluEkipamentu.objects.filter(ekipamentu__kategoria__id=x.id).count()
		obj2 = LabInventoryStock.objects.filter(inventory__kategoria__id=x.id).aggregate(total_sum=Sum('total_stock'))['total_sum']
		if obj2:
			obj2 = obj2
		else:
			obj2 = 0
		sumario_kategoria.append({
			"id_kategoria":x.hashed,
			"kategoria":x.kategoria,
			"totalEkipamentu":obj1,
			"totalInventaria":obj2
			})
	context = {
		"title":"Relatoriu Tabular Ekipamentu Laboratoriu","active_relatoriu":"active",
		"group":group,"listaDoador":listaDoador,
		"sumario_kategoria":sumario_kategoria,"sumario_doador":sumario_doador,
		"totalEkipamentu":totalEkipamentu,"totalInventory":totalInventory,
		"ekipamentuUzaHela":ekipamentuUzaHela,"ekipamentuDisponivel":ekipamentuDisponivel,
		"ekipamentuDiak":ekipamentuDiak,"ekipamentuAat":ekipamentuAat,
		"sumariu_inventaria_tuir_fulan_tinan_atual":sumariu_inventaria_tuir_fulan_tinan_atual,
		"sumariu_tuir_fulan_tinan_atual":sumariu_tuir_fulan_tinan_atual,
		"sumario_kada_tinan":sumario_kada_tinan,"sumario_inventaria_kada_tinan":sumario_inventaria_kada_tinan,
	}
	return render(request, "tabular/DashTabularReport.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def reportAllEquipments(request):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.all()
	
	context = {
		"title":"Relatoriu Lista Ekipamentu Laboratoriu",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def reportEkipamentuUza(request):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.filter(status='Uza Hela')
	context = {
		"title":"Relatoriu Lista Ekipamentu Laboratoriu Uza Hela",
		"active_relatoriu":"active",
		"group":group,
		"page":"uza hela",
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def reportEkipamentuDisponivel(request):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.filter(status='Disponivel')
	context = {
		"title":"Relatoriu Lista Ekipamentu Laboratoriu Disponivel",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def reportEkipamentuDiak(request):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.filter(kondisaun='Diak')
	context = {
		"title":"Relatoriu Tabular Ekipamentu Laboratoriu Kondisaun Diak",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def reportEkipamentuAat(request):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.filter(kondisaun='Aat')
	context = {
		"title":"Relatoriu Lista Ekipamentu Laboratoriu Kondisaun Aat",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportKategoriaEkipamentu(request,hashid):
	group = request.user.groups.all()[0].name
	cat = get_object_or_404(Kategoria,hashed=hashid)
	objects = DetalluEkipamentu.objects.filter(ekipamentu__kategoria__id=cat.id)
	context = {
		"title":f"Relatoriu Lista Ekipamentu Laboratoriu Kategoria {cat.kategoria}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportDoadorEkipamentu(request,hashid):
	group = request.user.groups.all()[0].name
	doador = get_object_or_404(Doadores,hashed=hashid)
	objects = DetalluEkipamentu.objects.filter(ekipamentu__doador__id=doador.id)
	context = {
		"title":f"Relatoriu Lista Ekipamentu Laboratoriu Doador {doador.doador}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportDoadorEkipamentuTuirFulan(request,idFulan,doadorID):
	group = request.user.groups.all()[0].name
	doador = get_object_or_404(Doadores,hashed=doadorID)
	objects = DetalluEkipamentu.objects.filter(ekipamentu__doador__id=doador.id,ekipamentu__data_simu__month=idFulan,ekipamentu__data_simu__year=date.today().year)
	context = {
		"title":f"Relatoriu Lista Ekipamentu Laboratoriu Doador {doador.doador} Fulan {getFulanNaran(int(idFulan))}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportEkipamentuTuirTinan(request,year):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.filter(ekipamentu__data_simu__year=year)
	context = {
		"title":f"Relatoriu Lista Ekipamentu Laboratoriu Tinan {year}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllequipments.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportKategoriaInventaria(request,hashid):
	group = request.user.groups.all()[0].name
	cat = get_object_or_404(Kategoria,hashed=hashid)
	objects = LabInventory.objects.filter(kategoria__id=cat.id)
	context = {
		"title":f"Relatoriu Lista Inventaria Laboratoriu Kategoria {cat.kategoria}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllinventaria.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportDoadorInventaria(request,hashid):
	group = request.user.groups.all()[0].name
	doador = get_object_or_404(Doadores,hashed=hashid)
	objects = LabInventory.objects.filter(doador__id=doador.id)
	context = {
		"title":f"Relatoriu Lista Inventaria Laboratoriu Doador {doador.doador}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllinventaria.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportInventariaTamaTuirFulan(request,idFulan):
	group = request.user.groups.all()[0].name
	objects = LabInventoryTransaction.objects.filter(data__month=idFulan,data__year=date.today().year).exclude(total_tama=0).order_by('-id')
	context = {
		"title":f"Relatoriu Lista Inventaria Laboratoriu Tama Fulan {getFulanNaran(int(idFulan))}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportInventariaTamaTuirFulan.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportInventariaSaiTuirFulan(request,idFulan):
	group = request.user.groups.all()[0].name
	objects = LabInventoryTransaction.objects.filter(data__month=idFulan,data__year=date.today().year).exclude(total_sai=0).order_by('-id')
	context = {
		"title":f"Relatoriu Lista Inventaria Laboratoriu Sai Fulan {getFulanNaran(int(idFulan))}",
		"active_relatoriu":"active",
		"group":group,
		"page":"inventariaSai",
		"objects":objects,
		
	}
	return render(request, "tabular/ReportInventariaSaiTuirFulan.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportInventariaTamaTuirTinan(request,year):
	group = request.user.groups.all()[0].name
	objects = LabInventoryTransaction.objects.filter(data__year=year).exclude(total_tama=0).order_by('-id')
	context = {
		"title":f"Relatoriu Lista Inventaria Laboratoriu Tama Tinan {year}",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportInventariaTamaTuirFulan.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def ReportInventariaSaiTuirTinan(request,year):
	group = request.user.groups.all()[0].name
	objects = LabInventoryTransaction.objects.filter(data__year=year).exclude(total_sai=0).order_by('-id')
	context = {
		"title":f"Relatoriu Lista Inventaria Laboratoriu Sai Tinan {year}",
		"active_relatoriu":"active",
		"group":group,
		"page":"inventariaSai",
		"objects":objects,
		
	}
	return render(request, "tabular/ReportInventariaSaiTuirFulan.html",context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def reportAllInventaria(request):
	group = request.user.groups.all()[0].name
	objects = LabInventory.objects.all()
	
	context = {
		"title":"Relatoriu Lista Inventaria Laboratoriu",
		"active_relatoriu":"active",
		"group":group,
		"objects":objects,
		
	}
	return render(request, "tabular/ReportAllinventaria.html",context)
