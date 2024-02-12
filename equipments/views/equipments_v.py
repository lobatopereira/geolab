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
def EquipmentsDash(request):
	group = request.user.groups.all()[0].name
	doadorlist = Doadores.objects.all()
	catlist = Kategoria.objects.all()
	catlist1 = Ekipamentu.objects.distinct().values('kategoria__id').all().order_by('kategoria__id')
	categorylist = []
	for x in catlist1:
		catItem = Kategoria.objects.get(id=x['kategoria__id'])
		categorylist.append(catItem)
	objects = Ekipamentu.objects.all()
	context = {
		'group':group,'objects': objects, 
		'active_equipments':'active',
		'active_equipment':'active',
		'doadorlist':doadorlist,'catlist':catlist,
		'categorylist':categorylist,'page':'dash',
		'title': 'Dashboard Ekipamentu Laboratoriu', 'legend': 'Dashboard Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/dash.html', context)


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def equipmentCategory(request,hashid):
	group = request.user.groups.all()[0].name
	category = get_object_or_404(Kategoria,hashed=hashid)
	doadorlist = Doadores.objects.all()
	catlist = Kategoria.objects.all()
	catlist1 = Ekipamentu.objects.distinct().values('kategoria__id').all().order_by('kategoria__id')
	categorylist = []
	for x in catlist1:
		catItem = Kategoria.objects.get(id=x['kategoria__id'])
		categorylist.append(catItem)
	objects = Ekipamentu.objects.filter(kategoria=category)
	context = {
	'group':group,'objects': objects, 
	'active_equipments':'active',
	'active_equipment':'active','doadorlist':doadorlist,
	'catlist':catlist,'page':'dash',
	'categorylist':categorylist,
	'title': f'Lista Ekipamentu Kategoria {category.kategoria}', 'legend': f'Lista Ekipamentu Kategoria {category.kategoria}',
	}
	return render(request, 'equipment_a/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def createEquipment(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid = getjustnewid(Ekipamentu)
		new_hashid = hash_md5(str(newid))
		ekipamentu = request.POST.get("ekipamentu")
		marka = request.POST.get("marka")
		data = request.POST.get("data")
		doador = request.POST.get("doador")
		doador = get_object_or_404(Doadores,id=doador)
		kategoria = request.POST.get("kategoria")
		kategoria = get_object_or_404(Kategoria,id=kategoria)
		obj3 = Ekipamentu.objects.create(id=newid,kategoria=kategoria,doador=doador,naran=ekipamentu,data_simu=data,marka=marka,hashed=new_hashid,user_created=request.user)
		messages.success(request, f'Dadus Ekipamentu Rejistu ho Susesu!')
		return redirect('EquipmentsDash')
	context = {
	'group': group,'active_kategoria':'active',
	'active_equipments':'active',
	'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def createEquipmentDetail(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Ekipamentu,hashed=hashid)
	objects_kuantity = DetalluEkipamentu.objects.filter(ekipamentu=objects).count()
	if request.method == 'POST' or request.method == 'FILES':
		if objects_kuantity < objects.kuantidade():
			newid = getjustnewid(DetalluEkipamentu)
			new_hashid = hash_md5(str(newid))
			serial = request.POST.get("serial")
			kondisaun = request.POST.get("kondisaun")
			status = request.POST.get("status")
			imajen = request.FILES.get("imajen")
			obj3 = DetalluEkipamentu.objects.create(id=newid,nu_serial=serial,kondisaun=kondisaun,ekipamentu=objects,status=status,hashed=new_hashid,user_created=request.user,image=imajen)
			messages.success(request, f'Dadus Nu. Serail Ekipamentu Rejistu ho Susesu!')
		else:
			messages.error(request, f'Rejistu la Susesu, Erro iha Kuantidade Ekipamentu!')
		return redirect('detailEquipment', objects.hashed)
	context = {
	'group': group,'active_kategoria':'active',
	'active_equipments':'active',
	'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def updateEquipmentDetail(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(DetalluEkipamentu,hashed=hashid)
	objects_kuantity = DetalluEkipamentu.objects.filter(ekipamentu=objects.ekipamentu).count()
	if request.method == 'POST' or request.method == 'FILES':
		objects.nu_serial = request.POST.get("serial")
		objects.kondisaun = request.POST.get("kondisaun")
		objects.status = request.POST.get("status")
		objects.image = request.FILES.get("imajen")
		objects.save()
		messages.success(request, f'Dadus Nu. Serail Ekipamentu Rejistu ho Susesu!')
		return redirect('detailEquipment', objects.ekipamentu.hashed)
	context = {
		# 'profile': profile, 'p_form': p_form,
		'active_kategoria':'active',
		'active_equipments':'active',
		'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def updateEquipment(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Ekipamentu,hashed=hashid)
	if request.method == 'POST':
		ekipamentu = request.POST.get("ekipamentu")
		marka = request.POST.get("marka")
		data = request.POST.get("data")
		doador = request.POST.get("doador")
		doador = get_object_or_404(Doadores,id=doador)
		kategoria = request.POST.get("kategoria")
		kategoria = get_object_or_404(Kategoria,id=kategoria)
		objects.naran=ekipamentu
		objects.marka=marka
		objects.data_simu=data
		objects.doador=doador
		objects.kategoria=kategoria
		objects.save()
		messages.success(request, f'Dadus Ekipamentu Altera ho Susesu!')
		return redirect('EquipmentsDash')
	context = {
		# 'profile': profile, 'p_form': p_form,
		'active_kategoria':'active',
		'active_equipments':'active',
		'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def detailEquipment(request,hashid):
	group = request.user.groups.all()[0].name
	doadorlist = Doadores.objects.all()
	catlist = Kategoria.objects.all()
	objects = get_object_or_404(Ekipamentu,hashed=hashid)
	objects1 = DetalluEkipamentu.objects.filter(ekipamentu=objects)
	kuantidade = objects1.count()
	context = {'group': group,'objects': objects,
		'objects1': objects1,'kuantidade': kuantidade,
		'active_kategoria':'active',
		'active_equipments':'active',
		'page':'detail','doadorlist':doadorlist,'catlist':catlist,
		'title': f'Detallu Ekipamentu Laboratoriu {objects.naran}', 'legend': f'Detallu Ekipamentu Laboratoriu {objects.naran}',
	}
	return render(request, 'equipment_a/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def createEquipmentQuantity(request,hashid):
	group = request.user.groups.all()[0].name
	ekipamentu = get_object_or_404(Ekipamentu,hashed=hashid)
	if request.method == 'POST':
		newid = getjustnewid(KuantidadeEkipamentu)
		new_hashid = hash_md5(str(newid))
		kuantidadeekipamentu = request.POST.get("kuantidadeekipamentu")
		obj3 = KuantidadeEkipamentu.objects.create(id=newid,ekipamentu=ekipamentu,kuantidade_inisiu=kuantidadeekipamentu,kuantidade_disponivel=kuantidadeekipamentu,kuantidade_empresta=0,hashed=new_hashid,user_created=request.user)
		messages.success(request, f'Dadus Kuantidade Ekipamentu {ekipamentu.naran} Konfigura ho Susesu!')
		return redirect('EquipmentsDash')
	context = {
	'group': group,'active_kategoria':'active',
		'active_equipments':'active',
		'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/dash.html', context)


# kokok serverside datatables
from django.http import JsonResponse
from django.views import View
from django.db.models import Q

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def EkipamentuListServerSide(request):
	context = {'active_kategoria':'active',
		'active_equipments':'active',
		'page':'dash',
		'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/serversideExample.html', context)


class EkipamentuListJson(View):
	def get(self, request, *args, **kwargs):
		# Handle DataTables parameters
		draw = int(request.GET.get('draw', 1))
		start = int(request.GET.get('start', 0))
		length = int(request.GET.get('length', 10))
		search_value = request.GET.get('search[value]', '')

		queryset = Ekipamentu.objects.all()
		# Filter your queryset based on search value
		if search_value:
			queryset = queryset.filter(
				Q(kategoria__kategoria__icontains=search_value) |
				Q(doador__doador__icontains=search_value) |
				Q(data_simu__icontains=search_value) |
				Q(naran__icontains=search_value) |
				Q(marka__icontains=search_value)
			)
		# Count total records
		total_records = queryset.count()

		# Apply pagination
		queryset = queryset[start:start + length]
		# Prepare the data in the required format
		data = [
		{
			'kategoria': item.kategoria.kategoria,
			'doador': item.doador.doador,
			'data_simu': item.data_simu.strftime("%Y-%m-%d") if item.data_simu else None,
			'naran': item.naran,
			'marka': item.marka,
			'hashed': item.hashed,
		}
			for item in queryset
		]
		# Prepare the response
		response_data = {
			'draw': draw,
			'recordsTotal': total_records,
			'recordsFiltered': total_records,
			'data': data,
		}
		return JsonResponse(response_data)	

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def EkipamentuListServerSide1(request):
	lista_categoria = Kategoria.objects.all()
	context = {'active_kategoria':'active',
		'active_equipments':'active',
		'page':'dash',
		'lista_categoria':lista_categoria,
		'title': 'Dadus Ekipamentu Laboratoriu', 'legend': 'Dadus Ekipamentu Laboratoriu',
	}
	return render(request, 'equipment_a/serversideExample1.html', context)


class EkipamentuListJson1(View):
	def get(self, request, *args, **kwargs):
		# Handle DataTables parameters
		draw = int(request.GET.get('draw', 1))
		start = int(request.GET.get('start', 0))
		length = int(request.GET.get('length', 10))
		search_kategoria = request.GET.get('search_kategoria', '')
		search_doador = request.GET.get('search_doador', '')

		# Filter queryset based on search values for kategoria and doador
		queryset = Ekipamentu.objects.all()
		if search_kategoria:
			queryset = queryset.filter(kategoria__kategoria__icontains=search_kategoria)
		if search_doador:
			queryset = queryset.filter(doador__doador__icontains=search_doador)


		total_records = queryset.count()

		# Apply pagination
		queryset = queryset[start:start + length]
		# Prepare the data in the required format
		data = [
            {
                'kategoria': item.kategoria.kategoria,
                'doador': item.doador.doador,
                'data_simu': item.data_simu.strftime("%Y-%m-%d") if item.data_simu else None,
                'naran': item.naran,
                'marka': item.marka,
                'hashed': item.hashed,
            }
            for item in queryset
        ]
		# Prepare the response
		response_data = {
			'draw': draw,
			'recordsTotal': total_records,
			'recordsFiltered': total_records,
			'data': data,
		}
		return JsonResponse(response_data)	