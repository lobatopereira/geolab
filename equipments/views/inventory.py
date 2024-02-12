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
from equipments.forms import *
from django.db import transaction
from custom.utils import *
from django.db.models import Q


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def InventoryDash(request):
	group = request.user.groups.all()[0].name
	doadorlist = Doadores.objects.all()
	catlist = Kategoria.objects.all()
	catlist1 = LabInventory.objects.distinct().values('kategoria__id').all().order_by('kategoria__id')
	categorylist = []
	for x in catlist1:
		catItem = Kategoria.objects.get(id=x['kategoria__id'])
		categorylist.append(catItem)
	objects = LabInventory.objects.all()
	context = {
		'objects': objects, 
		'group': group, 
		'active_inventory':'active',
		'doadorlist':doadorlist,
		'catlist':catlist,
		'categorylist':categorylist,
		'page':'dash',
		'title': 'Dashboard Inventaria Laboratoriu', 'legend': 'Dashboard Inventaria Laboratoriu',
	}
	return render(request, 'inventory/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def inventoryCategory(request,hashid):
	group = request.user.groups.all()[0].name
	category = get_object_or_404(Kategoria,hashed=hashid)
	doadorlist = Doadores.objects.all()
	catlist = Kategoria.objects.all()
	catlist1 = LabInventory.objects.distinct().values('kategoria__id').all().order_by('kategoria__id')
	categorylist = []
	for x in catlist1:
		catItem = Kategoria.objects.get(id=x['kategoria__id'])
		categorylist.append(catItem)
	objects = LabInventory.objects.filter(kategoria=category)
	context = {
		'objects': objects, 
		'group': group, 
		'active_inventory':'active',
		'doadorlist':doadorlist,
		'catlist':catlist,
		'categorylist':categorylist,
		'page':'dash',
		'title': f'Lista Inventaria Kategoria {category.kategoria}', 'legend': f'Lista Inventaria Kategoria {category.kategoria}',
	}
	return render(request, 'inventory/dash.html', context)


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def createInventory(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST' or request.method == 'FILES':
		newid = getjustnewid(LabInventory)
		new_hashid = hash_md5(str(newid))
		ekipamentu = request.POST.get("ekipamentu")
		marka = request.POST.get("marka")
		if request.POST.get("data"):
			data = request.POST.get("data")
		else:
			messages.warning(request, f'Favor prense Data!')
			return redirect('InventoryDash')
		doador = request.POST.get("doador")
		total_tama = request.POST.get("total_tama")
		kodigu_stock = request.POST.get("kodigu_stock")
		doador = get_object_or_404(Doadores,id=doador)
		kategoria = request.POST.get("kategoria")
		imajen = request.FILES.get("imajen")
		kategoria = get_object_or_404(Kategoria,id=kategoria)
		obj3 = LabInventory.objects.create(id=newid,kategoria=kategoria,doador=doador,naran=ekipamentu,dataTama=data,marka=marka,hashed=new_hashid,user_created=request.user,image=imajen)
		newid1 = getjustnewid(LabInventoryStock)
		new_hashid1 = hash_md5(str(newid1))
		obj4 = LabInventoryStock.objects.create(id=newid1,hashed=new_hashid1,user_created=request.user,inventory=obj3,total_tama=total_tama,kodigu_stock=kodigu_stock,total_sai=0,total_stock=total_tama)
		newid2 = getjustnewid(LabInventoryTransaction)
		new_hashid2 = hash_md5(str(newid2))
		obj5 = LabInventoryTransaction.objects.create(id=newid2,hashed=new_hashid2,user_created=request.user,inventory=obj3,data=data,total_tama=total_tama,total_sai=0,total=total_tama)
		messages.success(request, f'Dadus Inventaria Rejistu ho Susesu!')
		return redirect('InventoryDash')
	context = {
		'group': group,
		'active_inventory':'active',
		'title': 'Dadus Inventaria Laboratoriu', 'legend': 'Dadus Inventaria Laboratoriu',
	}
	return render(request, 'inventory/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def updateInventory(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(LabInventory,hashed=hashid)
	if request.method == 'POST' or request.method == 'FILES':
		ekipamentu = request.POST.get("ekipamentu")
		marka = request.POST.get("marka")
		if request.POST.get("data"):
			data = request.POST.get("data")
		else:
			messages.warning(request, f'Favor prense Data!')
			return redirect('InventoryDash')
		doador = request.POST.get("doador")
		imajen = request.FILES.get("imajen")
		doador = get_object_or_404(Doadores,id=doador)
		kategoria = request.POST.get("kategoria")
		kategoria = get_object_or_404(Kategoria,id=kategoria)
		objects.naran=ekipamentu
		objects.marka=marka
		objects.dataTama=data
		objects.image=imajen
		objects.doador=doador
		objects.kategoria=kategoria
		objects.save()
		messages.success(request, f'Dadus Inventaria Altera ho Susesu!')
		return redirect('InventoryDash')
	context = {
		'group': group,
		'active_inventory':'active',
		'title': 'Dadus Inventaria Laboratoriu', 'legend': 'Dadus Inventaria Laboratoriu',
	}
	return render(request, 'inventory/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def detailInventory(request,hashid):
	group = request.user.groups.all()[0].name
	doadorlist = Doadores.objects.all()
	catlist = Kategoria.objects.all()
	objects = get_object_or_404(LabInventory,hashed=hashid)
	objects1 = LabInventoryTransaction.objects.filter(inventory=objects).order_by('-id')
	context = {
		'group': group,
		'objects': objects,
		'objects1': objects1,
		'active_inventory':'active',
		'page':'detail',
		'doadorlist':doadorlist,
		'catlist':catlist,
		'title': f'Detallu Inventaria Laboratoriu {objects.naran}', 'legend': f'Detallu Inventaria Laboratoriu {objects.naran}',
	}
	return render(request, 'inventory/dash.html', context)


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def registerInventoryKuantityIn(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(LabInventory,hashed=hashid)
	if request.method == 'POST' or request.method == 'FILES':
		if request.POST.get("data"):
			data = request.POST.get("data")
		else:
			messages.warning(request, f'Favor prense Data!')
			return redirect('InventoryDash')
		total_tama = request.POST.get("total_tama")

		obj4 = LabInventoryStock.objects.get(inventory=objects)
		obj4.total_tama += int(total_tama)
		obj4.total_stock += int(total_tama)
		obj4.total_sai = 0 
		obj4.save()
		newid2 = getjustnewid(LabInventoryTransaction)
		new_hashid2 = hash_md5(str(newid2))
		lastTransac = LabInventoryTransaction.objects.filter(inventory=objects).last()
		if lastTransac:
			total_tama_t = int(total_tama) + lastTransac.total
		else:
			total_tama_t = int(total_tama) + 0
		obj5 = LabInventoryTransaction.objects.create(id=newid2,hashed=new_hashid2,user_created=request.user,inventory=objects,data=data,total_tama=total_tama,total_sai=0,total=total_tama_t)
		messages.success(request, f'Dadus Kuantidade Inventaria {objects.naran} ho Kodigu Stock {objects.inventoryStock.kodigu_stock}, Rejistu ho Susesu!')
		return redirect('InventoryDash')
	context = {'group': group,'active_inventory':'active',
		'title': 'Dadus Inventaria Laboratoriu', 'legend': 'Dadus Inventaria Laboratoriu',
	}
	return render(request, 'inventory/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def InventoryUzaDash(request):
	group = request.user.groups.all()[0].name
	results = []
	if request.method == 'GET':
		search_query = request.GET.get('search_inventory', '').strip()
		if search_query:
			results = LabInventory.objects.filter(
				Q(naran__icontains=search_query) | Q(inventoryStock__kodigu_stock__icontains=search_query) 
			)
	
	context = {
		'group': group,
		'resultadu': results,
		'page': "dash",
		'active_uzainventory':'active',
		'active_inventory':'active',
		'title': 'Formulariu Uza Inventaria', 'legend': 'Formulariu Uza Inventaria',
	}
	return render(request, 'inventory/UzaInventoryDash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def UzaInventory(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(LabInventory,hashed=hashid)
	if request.method == 'POST':
		newid = getjustnewid(LabInventoryTransaction)
		new_hashid = hash_md5(str(newid))
		form = UtilizaInventoryForm(request.POST, request.FILES)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.id = newid
				instance.hashed = new_hashid
				instance.user_created = request.user
				instance.inventory = objects
				instance.total_tama = 0
				total_sai = int(instance.total_sai)
				lastTransac = LabInventoryTransaction.objects.filter(inventory=objects).last()
				if lastTransac:
					total_t = lastTransac.total - int(total_sai)
				else:
					total_t = 0
				instance.total = total_t 
				obj4 = LabInventoryStock.objects.get(inventory=objects)
				obj4.total_tama = 0
				obj4.total_stock -= int(total_sai)
				obj4.total_sai += int(total_sai)
				obj4.save()
				instance.save() 
				messages.success(request, f'Dadus Uza Inventaria {objects.naran} rejista ona.')
				return redirect('InventoryUzaDash')
	else:
		form = UtilizaInventoryForm()
	context = {
		'group': group,
		'page': "form",
		'form': form,
		'objects': objects,
		'active_uzainventory':'active',
		'active_inventory':'active',
		'title': f'Formulariu Uza Inventaria {objects.naran}', 'legend': f'Formulariu Uza Inventaria {objects.naran}',
	}
	return render(request, 'inventory/UzaInventoryDash.html', context)
