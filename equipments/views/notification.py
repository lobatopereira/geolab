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
from datetime import datetime, timedelta

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def notifUsedDeadlineList(request):
	group = request.user.groups.all()[0].name
	results = UtilizaEkipamentu.objects.filter(data_atu_entrega__lte=datetime.now(),is_return=False,item__status = 'Uza Hela').all()
	context = {
		'group':group,
		'resultadu': results,
		'page': "dash",
		'active_entrega':'active',
		'active_utilizador':'active',
		'title': 'Lista Utilizasaun Ekipamentu Liu ona Loron atu Entrega', 'legend': 'Lista Utilizasaun Ekipamentu Liu ona Loron atu Entrega',
	}
	return render(request, 'entrega_ekipamentu/dash.html', context)

@login_required
@allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
def notifUsedDeadlineAbanList(request):
	group = request.user.groups.all()[0].name
	results = UtilizaEkipamentu.objects.filter(data_atu_entrega=datetime.now() + timedelta(days=1),is_return=False,item__status='Uza Hela').all()
	context = {
		'group':group,
		'resultadu': results,
		'page': "dash",
		'active_entrega':'active',
		'active_utilizador':'active',
		'title': 'Lista Utilizasaun Ekipamentu atu Entrega iha Aban', 'legend': 'Lista Utilizasaun Ekipamentu atu Entrega iha Aban',
	}
	return render(request, 'entrega_ekipamentu/dash.html', context)
