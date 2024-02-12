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
from equipments.forms import *
from django.db.models import Q
from django.db import transaction


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def UtilizadorEquipmentuDash(request):
	group = request.user.groups.all()[0].name
	objects = Utilizador.objects.all()
	total_utilizador = objects.count()
	total_utilizador_uza_ekip = UtilizaEkipamentu.objects.filter(is_return=False).distinct().values('utilizador').count()

	context = {
		'group':group,
		'objects': objects,
		'total_utilizador': total_utilizador,
		'total_utilizador_uza_ekip': total_utilizador_uza_ekip,
		'page': "dash",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Dadus Utilizadores Ekipamentu', 'legend': 'Dadus Utilizadores Ekipamentu',
	}
	return render(request, 'utilizador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def HistoriaUtilazaEkipamentuLaboratoriu(request):
	group = request.user.groups.all()[0].name
	objects = UtilizaEkipamentu.objects.all()
	disponivel = DetalluEkipamentu.objects.filter(status='Disponivel').all()
	total_disponivel = disponivel.count()
	la_disponivel = DetalluEkipamentu.objects.filter(status='Uza Hela').all()
	total_la_disponivel = la_disponivel.count()
	total_utilizador = objects.count()
	total_utilizador_uza_ekip = UtilizaEkipamentu.objects.filter(is_return=False).distinct().values('utilizador').count()
	context = {
		'group':group,
		'objects': objects,
		'la_disponivel': la_disponivel,
		'disponivel': disponivel,
		'total_utilizador_uza_ekip': total_utilizador_uza_ekip,
		'total_utilizador': total_utilizador,
		'page': "historiaUzaEkipamentuList",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Dadus Historia Utiliza Ekipamentu Laboratoriu', 'legend': 'Dadus Historia Utiliza Ekipamentu Laboratoriu',
	}
	return render(request, 'uza_ekipamentu/historia.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def UtilizadorEquipmentuDetail(request,hashid):
	group = request.user.groups.all()[0].name
	utilizadorData = Utilizador.objects.get(hashed=hashid)
	objects = Utilizador.objects.all()
	total_utilizador = objects.count()
	historiaUzaEkipamentu = UtilizaEkipamentu.objects.filter(utilizador=utilizadorData,is_return=True)
	ekipamentuUzaHela = UtilizaEkipamentu.objects.filter(utilizador=utilizadorData,is_return=False,item__status='Uza Hela')
	historiaUzaInventaria = LabInventoryTransaction.objects.filter(utilizador=utilizadorData)
	total_utilizador_uza_ekip = UtilizaEkipamentu.objects.filter(is_return=False).distinct().values('utilizador').count()
	context = {
		'group':group,
		'objects': objects,
		'utilizadorData': utilizadorData,
		'total_utilizador': total_utilizador,
		'historiaUzaEkipamentu': historiaUzaEkipamentu,
		'historiaUzaInventaria': historiaUzaInventaria,
		'ekipamentuUzaHela': ekipamentuUzaHela,
		'total_utilizador_uza_ekip': total_utilizador_uza_ekip,
		'page': "detail",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': f'Detallu Utilizador {utilizadorData.naran}', 'legend': f'Detallu Utilizador {utilizadorData.naran}',
	}
	return render(request, 'utilizador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def HistoriaUtilizaEquipmentu(request,hashid):
	group = request.user.groups.all()[0].name
	utilizadorData = Utilizador.objects.get(hashed=hashid)
	objects = Utilizador.objects.all()
	total_utilizador = objects.count()
	historiaUzaEkipamentu = UtilizaEkipamentu.objects.filter(utilizador=utilizadorData,is_return=True)
	ekipamentuUzaHela = UtilizaEkipamentu.objects.filter(utilizador=utilizadorData,is_return=False,item__status='Uza Hela')
	historiaUzaInventaria = LabInventoryTransaction.objects.filter(utilizador=utilizadorData)
	total_utilizador_uza_ekip = UtilizaEkipamentu.objects.filter(is_return=False).distinct().values('utilizador').count()
	context = {
		'group':group,
		'objects': objects,
		'utilizadorData': utilizadorData,
		'total_utilizador': total_utilizador,
		'historiaUzaEkipamentu': historiaUzaEkipamentu,
		'historiaUzaInventaria': historiaUzaInventaria,
		'ekipamentuUzaHela': ekipamentuUzaHela,
		'page': "detailhistoria",
		'total_utilizador_uza_ekip': total_utilizador_uza_ekip,
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': f'Detallu Utilizador {utilizadorData.naran}', 'legend': f'Detallu Utilizador {utilizadorData.naran}',
	}
	return render(request, 'utilizador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def HistoriaUtilizaInventory(request,hashid):
	group = request.user.groups.all()[0].name
	utilizadorData = Utilizador.objects.get(hashed=hashid)
	objects = Utilizador.objects.all()
	total_utilizador = objects.count()
	historiaUzaEkipamentu = UtilizaEkipamentu.objects.filter(utilizador=utilizadorData,is_return=True)
	ekipamentuUzaHela = UtilizaEkipamentu.objects.filter(utilizador=utilizadorData,is_return=False,item__status='Uza Hela')
	historiaUzaInventaria = LabInventoryTransaction.objects.filter(utilizador=utilizadorData)
	total_utilizador_uza_ekip = UtilizaEkipamentu.objects.filter(is_return=False).distinct().values('utilizador').count()
	context = {
		'group':group,
		'objects': objects,
		'utilizadorData': utilizadorData,
		'total_utilizador': total_utilizador,
		'total_utilizador_uza_ekip': total_utilizador_uza_ekip,
		'historiaUzaEkipamentu': historiaUzaEkipamentu,
		'historiaUzaInventaria': historiaUzaInventaria,
		'ekipamentuUzaHela': ekipamentuUzaHela,
		'page': "detailhistoria1",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': f'Detallu Utilizador {utilizadorData.naran}', 'legend': f'Detallu Utilizador {utilizadorData.naran}',
	}
	return render(request, 'utilizador/dash.html', context)


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def DetailDetalluEquipment(request,hashid):
	group = request.user.groups.all()[0].name
	objects = DetalluEkipamentu.objects.get(hashed=hashid)
	disponivel = DetalluEkipamentu.objects.filter(status='Disponivel').all()
	total_disponivel = disponivel.count()
	la_disponivel = DetalluEkipamentu.objects.filter(status='Uza Hela').all()
	total_la_disponivel = la_disponivel.count()
	historiaUzaEkipamentu = UtilizaEkipamentu.objects.filter(item=objects).order_by('-data_empresta')
	total_utilizador_uza_ekip = UtilizaEkipamentu.objects.filter(is_return=False).distinct().values('utilizador').count()
	context = {
		'group':group,
		'objects': objects,
		'total_disponivel': total_disponivel,
		'total_la_disponivel': total_la_disponivel,
		'historiaUzaEkipamentu': historiaUzaEkipamentu,
		'total_utilizador_uza_ekip': total_utilizador_uza_ekip,
		'page': "detailhistoriaDetalluEkipamentu",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': f'Detallu Ekipamentu {objects.ekipamentu.naran}', 'legend': f'Detallu Ekipamentu {objects.ekipamentu.naran}',
	}
	return render(request, 'uza_ekipamentu/dash.html', context)


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def UtilizadorEquipmentuAdd(request):
	group = request.user.groups.all()[0].name
	total_utilizador = Utilizador.objects.all().count()
	if request.method == 'POST':
		newid = getjustnewid(Utilizador)
		new_hashid = hash_md5(str(newid))
		form = UtilizadorForm(request.POST, request.FILES)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.id = newid
				instance.hashed = new_hashid
				instance.datetime = datetime.datetime.now()
				instance.user_created = request.user
				instance.save()
				messages.success(request, f'Dadus Utilizador Foun aumenta ona.')
				return redirect('UtilizadorEquipmentuDash')
	else:
		form = UtilizadorForm()
	context = {
		'group':group,
		'form': form,
		'total_utilizador': total_utilizador,
		'page': "utilizador_form",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Formulariu Rejistu Utilizador', 'legend': 'Formulariu Rejistu Utilizador',
	}
	return render(request, 'utilizador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def UtilizadorEquipmentuUpdate(request,hashid):
	group = request.user.groups.all()[0].name
	total_utilizador = Utilizador.objects.all().count()
	objects = Utilizador.objects.get(hashed=hashid)
	if request.method == 'POST':
		form = UtilizadorForm(request.POST, request.FILES,instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Dadus Utilizador altera ho susesu.')
			return redirect('UtilizadorEquipmentuDash')
	else:
		form = UtilizadorForm(instance=objects)
	context = {
		'group':group,
		'form': form,
		'total_utilizador': total_utilizador,
		'page': "utilizador_form",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Formulariu Altera Utilizador', 'legend': 'Formulariu Altera Utilizador',
	}
	return render(request, 'utilizador/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def UtilizadorUzaEquipmentuDash(request):
	group = request.user.groups.all()[0].name
	disponivel = DetalluEkipamentu.objects.filter(status='Disponivel').all()
	total_disponivel = disponivel.count()
	la_disponivel = DetalluEkipamentu.objects.filter(status='Uza Hela').all()
	total_la_disponivel = la_disponivel.count()
	form = EquipmentSearchForm()
	results = []
	if request.method == 'GET':
		search_query = request.GET.get('search_equipment', '').strip()
		if search_query:
			results = DetalluEkipamentu.objects.filter(
				Q(ekipamentu__naran__icontains=search_query) | Q(nu_serial__icontains=search_query)
			)
	context = {
		'group':group,
		'form': form,
		'resultadu': results,
		'disponivel': disponivel,
		'total_disponivel': total_disponivel,
		'la_disponivel': la_disponivel,
		'total_la_disponivel': total_la_disponivel,
		'page': "dash",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Dadus Uza Ekipamentu', 'legend': 'Dadus Uza Ekipamentu',
	}
	return render(request, 'uza_ekipamentu/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def UtilizadorEntregaEquipmentuDash(request):
	group = request.user.groups.all()[0].name
	form = EquipmentSearchForm()
	results = []
	if request.method == 'GET':
		search_query = request.GET.get('search_equipment', '').strip()
		if search_query:
			results = UtilizaEkipamentu.objects.filter(item__status='Uza Hela',data_entrega__isnull = True).filter(
				Q(item__ekipamentu__naran__icontains=search_query) | Q(item__nu_serial__icontains=search_query) | Q(utilizador__naran__icontains=search_query)
			)
	
	print('results:',results)
	context = {
		'group':group,
		'form': form,
		'resultadu': results,
		'page': "dash",
		'active_entrega':'active',
		'active_utilizador':'active',
		'title': 'Formulariu Entrega Ekipamentu', 'legend': 'Formulariu Entrega Ekipamentu',
	}
	return render(request, 'entrega_ekipamentu/dash.html', context)

@login_required
def UtilizadorUzaEquipmentuEmpresta(request,hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(DetalluEkipamentu,hashed=hashid)
	ekipamentu = get_object_or_404(Ekipamentu,hashed=objects.ekipamentu.hashed)
	disponivel = DetalluEkipamentu.objects.filter(status='Disponivel').all()
	total_disponivel = disponivel.count()
	la_disponivel = DetalluEkipamentu.objects.filter(status='Uza Hela').all()
	total_la_disponivel = la_disponivel.count()
	if request.method == 'POST':
		if objects.status == 'Disponivel':
			newid = getjustnewid(UtilizaEkipamentu)
			new_hashid = hash_md5(str(newid))
			form = UtilizaEkipamentuForm(request.POST, request.FILES)
			if form.is_valid():
				with transaction.atomic():
					instance = form.save(commit=False)
					instance.id = newid
					instance.hashed = new_hashid
					instance.ekipamentu = ekipamentu
					total_loron_atu_uza1 =  instance.data_atu_entrega - instance.data_empresta
					instance.total_loron_atu_uza = total_loron_atu_uza1.days
					instance.item = objects
					instance.user_created = request.user
					if instance.data_atu_entrega < instance.data_empresta:
						messages.warning(request, f'Favor Ajusta Data. Data atu Entrega fila fali Ekipamentu labele kiik liu Data Empresta')
						return redirect('UtilizadorUzaEquipmentuEmpresta',hashid)
					else:
						instance.save()
						objects.status = 'Uza Hela'
						objects.save()
						messages.success(request, f'Dadus Empresta ka uza ekipamentu rejista ona.')
						return redirect('UtilizadorUzaEquipmentuDash')
		else:
			messages.error(request, f'Dadus Ekipamentu {objects.ekipamentu.naran} ho Numeru serial {objects.nu_serial}, estadu {objects.status}.')
			return redirect('UtilizadorUzaEquipmentuDash')

	else:
		form = UtilizaEkipamentuForm()

	# print('results:',results)
	context = {
		'group':group,
		'form': form,
		'objects': objects,
		'disponivel': disponivel,
		'total_disponivel': total_disponivel,
		'la_disponivel': la_disponivel,
		'total_la_disponivel': total_la_disponivel,
		'page': "form",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Formulariu Empresta ka Uza Ekipamentu', 'legend': 'Formulariu Empresta ka Uza Ekipamentu',
	}
	return render(request, 'uza_ekipamentu/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def EntregaEkipamentu(request,hashid):
	group = request.user.groups.all()[0].name
	objects1 = get_object_or_404(UtilizaEkipamentu,hashed=hashid)
	objects = get_object_or_404(DetalluEkipamentu,hashed=objects1.item.hashed)
	# ekipamentu = get_object_or_404(Ekipamentu,hashed=objects.ekipamentu.hashed)
	# disponivel = DetalluEkipamentu.objects.filter(status='Disponivel').all()
	# total_disponivel = disponivel.count()
	# la_disponivel = DetalluEkipamentu.objects.filter(status='Uza Hela').all()
	# total_la_disponivel = la_disponivel.count()
	if request.method == 'POST':
		if objects.status == 'Uza Hela':
			form = EntregaEkipamentuForm(request.POST, request.FILES,instance=objects1)
			if form.is_valid():
				with transaction.atomic():
					instance = form.save(commit=False)
					totalLoronKontra = instance.data_entrega - objects1.data_atu_entrega
					instance.total_loron_kontra = totalLoronKontra.days
					instance.is_return = True
					if instance.data_entrega < objects1.data_empresta:
						messages.warning(request, f'Favor Ajusta Data Entrega. Data Entrega labele kiik liu Data Empresta')	
						return redirect('EntregaEkipamentu',objects1.hashed)
					else:
						instance.save()
						objects.status = 'Disponivel'
						kondisaunDepois = instance.kondisaun
						objects.kondisaun = kondisaunDepois
						objects.save()
						messages.success(request, f'Dadus ekipamentu {objects.ekipamentu.naran}, Entrega fali ona.')
						return redirect('UtilizadorUzaEquipmentuDash')
		else:
			messages.error(request, f'Dadus Ekipamentu {objects.ekipamentu.naran} ho Numeru serial {objects.nu_serial}, estadu {objects.status}.')
			return redirect('UtilizadorUzaEquipmentuDash')
	else:
		form = EntregaEkipamentuForm(instance=objects1)
	context = {
		'group':group,
		'form': form,
		'objects': objects,
		'objects1': objects1,
		'page': "form",
		'active_utilizador':'active',
		'active_utilizador':'active',
		'title': 'Formulariu Entrega Ekipamentu', 'legend': 'Formulariu Entrega Ekipamentu',
	}
	return render(request, 'uza_ekipamentu/entrega.html', context)


@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio'])
def UtilizadorEmprestaEquipmentu(request,hashid):
	group = request.user.groups.all()[0].name
	utilizadorData = get_object_or_404(Utilizador,hashed=hashid)
	disponivel = DetalluEkipamentu.objects.filter(status='Disponivel').all()
	total_disponivel = disponivel.count()
	la_disponivel = DetalluEkipamentu.objects.filter(status='Uza Hela').all()
	total_la_disponivel = la_disponivel.count()
	if request.method == 'POST':
		newid = getjustnewid(UtilizaEkipamentu)
		new_hashid = hash_md5(str(newid))
		form = UtilizadorEmprestaEkipamentuForm(request.POST, request.FILES)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.id = newid
				instance.hashed = new_hashid
				detEkipamentu = instance.item.hashed
				objects = get_object_or_404(DetalluEkipamentu,hashed=detEkipamentu)
				ekipamentu = get_object_or_404(Ekipamentu,hashed=objects.ekipamentu.hashed)
				if objects.status == 'Disponivel':
					instance.utilizador = utilizadorData
					instance.ekipamentu = ekipamentu
					total_loron_atu_uza1 =  instance.data_atu_entrega - instance.data_empresta
					instance.total_loron_atu_uza = total_loron_atu_uza1.days
					instance.item = objects
					instance.user_created = request.user
					if instance.data_atu_entrega < instance.data_empresta:
						messages.warning(request, f'Favor Ajusta Data. Data atu Entrega fila fali Ekipamentu labele kiik liu Data Empresta')
						return redirect('UtilizadorEmprestaEquipmentu',hashid)
					else:
						instance.save()
						objects.status = 'Uza Hela'
						objects.save()
						messages.success(request, f'Dadus Empresta ka uza ekipamentu rejista ona.')
						return redirect('UtilizadorUzaEquipmentuDash')
				else:
					messages.error(request, f'Dadus Ekipamentu {objects.ekipamentu.naran} ho Numeru serial {objects.nu_serial}, estadu {objects.status}.')
					return redirect('UtilizadorUzaEquipmentuDash')
	else:
		form = UtilizadorEmprestaEkipamentuForm()
	context = {'group':group,'form': form,
	'disponivel': disponivel,'total_disponivel': total_disponivel,
	'la_disponivel': la_disponivel,'total_la_disponivel': total_la_disponivel,
	'page': "formUtilizadorEmpresta",'active_utilizador':'active','active_utilizador':'active',
	'title': 'Formulariu Empresta ka Uza Ekipamentu', 'legend': 'Formulariu Empresta ka Uza Ekipamentu',}
	return render(request, 'uza_ekipamentu/dash.html', context)