import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import Municipality
from custom.utils import *
from users.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from users.models import Profile,AuditLogin
from users.forms import ProfileUpdateForm,UserForm
from rest_framework.response import Response


@login_required
def ProfileUpdate(request):
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		p_form = ProfileUpdateForm(request.POST,request.FILES, instance=profile)
		if p_form.is_valid():
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('user-profile')
	else:
		p_form = ProfileUpdateForm(instance=profile)

	context = {
		'profile': profile, 'p_form': p_form,
		'title': 'Perfil', 'legend': 'Perfil',
	}
	return render(request, 'account/profile.html', context)


@login_required
def AccountUpdate(request):
	group = request.user.groups.all()[0].name
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		u_form = UserForm(request.POST, instance=request.user)
		if u_form.is_valid():
			print("tama")
			u_form.save()
			messages.success(request, f'Ita boot nia konta altera ona!')
			return redirect('user-account')
	else:
		u_form = UserForm(instance=request.user)
	context = {
		'u_form': u_form,'profile': profile,
		'title': 'Info Konta', 'legend': 'Info Konta',
	}
	return render(request, 'account/account_settings.html', context)

class UserPasswordChangeView(PasswordChangeView):
	template_name = 'account/change_password.html'
	success_url = reverse_lazy('user-change-password-done')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['profile'] = Profile.objects.get(user=self.request.user)
		return context

class UserPasswordChangeDoneView(PasswordResetDoneView):
	template_name = 'account/change_password_done.html'


from django.contrib.auth.hashers import check_password

@login_required
@allowed_users(allowed_roles=['Admin'])
def UserList(request):
	group = request.user.groups.all()[0].name
	objects = []
	objects1 = User.objects.all()
	allGroup = Group.objects.all().exclude(name='Admin')
	grouplist = Group.objects.annotate(user_count=Count('user')).order_by('name')
	for x in objects1:
		stored_password = x.password
		is_valid_match = check_password('password', stored_password)
		if is_valid_match:
			objects.append([x,"password"])
		else:
			objects.append([x,"alteradu"])
	context = {
		'group': group,'allGroup': allGroup, 'objects': objects,'grouplist': grouplist,
		'accountListActive': 'active','title': 'Lista Utilizador', 'legend': 'Lista Utilizador'
	}
	return render(request, 'users/userlist.html', context)

@login_required
def user_with_group(request,id):
	group = request.user.groups.all()[0].name
	groupData = get_object_or_404(Group,id=id)
	objects = []
	objects1 = User.objects.filter(groups=groupData)
	allGroup = Group.objects.all().exclude(name='Admin')
	grouplist = Group.objects.annotate(user_count=Count('user')).order_by('name')
	for x in objects1:
		stored_password = x.password
		is_valid_match = check_password('password', stored_password)
		if is_valid_match:
			objects.append([x,"password"])
		else:
			objects.append([x,"alteradu"])

	
	context = {
		'group': group,'allGroup': allGroup, 'objects': objects,'grouplist': grouplist,
		'accountListActive': 'active','title': 'Lista Utilizador', 'legend': 'Lista Utilizador'
	}
	return render(request, 'users/userlist.html', context)

@login_required
def AccountLoginHistory(request):
	group = request.user.groups.all()[0].name
	objects = AuditLogin.objects.filter(user=request.user)
	profile = Profile.objects.get(user=request.user)
	context = {
		'group': group, 'objects': objects,'profile': profile,
		'accountLoginHistory': 'active','title': 'Historia Login', 'legend': 'Historia Login'
	}
	return render(request, 'account/login_history.html', context)

@login_required
@allowed_users(allowed_roles=['Admin'])
def createUser(request):
	group = request.user.groups.all()[0].name
	objects = User.objects.all()
	allGroup = Group.objects.all().exclude(name='Admin')
	grouplist = Group.objects.annotate(user_count=Count('user')).order_by('name')
	if request.method == 'POST':
		userGoup = request.POST.get("user_group")
		username = request.POST.get("username")
		apelido = request.POST.get("apelido")
		dob = request.POST.get("dob")
		password = make_password('password')
		username = split_string(username) + split_string(apelido)
		obj2 = User(username=username, password=password,is_active=False)
		obj2.save()
		group_user = Group.objects.get(id=str(userGoup))
		user = User.objects.get(id=obj2.id)
		user.groups.add(group_user)
		messages.success(request, f'Dadus Utilizador Rejistu ho Susesu!')
		return redirect('userlist')
	context = {
		'group': group,'allGroup': allGroup, 'objects': objects,'grouplist': grouplist,
		'accountListActive': 'active','title': 'Lista Utilizador', 'legend': 'Lista Utilizador'
	}
	return render(request, 'users/userlist.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def ativuUser(request,id):
	userData = get_object_or_404(User,id=id)
	userData.is_active = True
	userData.save()
	messages.success(request, f'User {userData.username} Ativu ho Susesu!')
	return redirect('userlist')

@login_required
@allowed_users(allowed_roles=['Admin'])
def desativuUser(request,id):
	userData = get_object_or_404(User,id=id)
	userData.is_active = False
	userData.save()
	messages.success(request, f'User {userData.username} Desativu ho Susesu!')
	return redirect('userlist')


@login_required
@allowed_users(allowed_roles=['Admin'])
def resetUserPassword(request,id):
	userData = get_object_or_404(User,id=id)
	password = make_password('password')
	userData.password = password
	userData.save()
	messages.success(request, f'Password ba {userData.username} Reset ho Susesu!')
	return redirect('userlist')

from users.admin import *
from equipments.admin import *
from custom.admin import *
import zipfile
@login_required
@allowed_users(allowed_roles=['Admin'])
def BackupDadusGEOLAB(request):
	today = datetime.date.today()
	naran_file =  "GEOLAB_" + str("backup_") + str(today) +"_"+ ".zip"
	# users 
	dataset01 = GroupResource().export()
	dataset02 = UserResource().export()
	dataset03 = ProfileResource().export()
	dataset04 = AuditLoginResource().export()
	# custom
	dataset1 = CountryResource().export()
	dataset2 = MunicipalityResource().export()
	dataset3 = AdministrativePostResource().export()
	dataset4 = VillageResource().export()
	dataset5 = AcademicLevelResource().export()
	dataset6 = ProfessionResource().export()
	# ekipamentu
	dataset7 = KategoriaResource().export()
	dataset8 = DoadoresResource().export()
	dataset9 = EkipamentuResource().export()
	dataset10 = KuantidadeEkipamentuResource().export()
	dataset11 = DetalluEkipamentuResource().export()
	dataset12 = UtilizadorResource().export()
	dataset13 = UtilizaEkipamentuResource().export()
	dataset14 = LabInventoryResource().export()
	dataset15 = LabInventoryStockResource().export()
	dataset16 = LabInventoryTransactionResource().export()

	with zipfile.ZipFile("media/dadusbackup/"+naran_file, 'w') as csv_zip:
		# users
		csv_zip.writestr("_01-Dadus_Groups.csv", dataset01.csv)
		csv_zip.writestr("_02-Dadus_Users.csv", dataset02.csv)
		csv_zip.writestr("_03-Dadus_Profiles.csv", dataset03.csv)
		csv_zip.writestr("_04-Dadus_AuditLogin.csv", dataset04.csv)
		# custom
		csv_zip.writestr("1-Dadus_Custom_Country.csv", dataset1.csv)
		csv_zip.writestr("2-Dadus_Custom_Munisipiu.csv", dataset2.csv)
		csv_zip.writestr("3-Dadus_Custom_Postu.csv", dataset3.csv)
		csv_zip.writestr("4-Dadus_Custom_Suku.csv", dataset4.csv)
		csv_zip.writestr("5-Dadus_Custom_Nivel_academiku.csv", dataset5.csv)
		csv_zip.writestr("6-Dadus_Custom_Profisaun.csv", dataset6.csv)
		# entrevistador
		csv_zip.writestr("7-Dadus_Kategoria.csv", dataset7.csv)
		# ema lakon
		csv_zip.writestr("8-Dadus_Doadores.csv", dataset8.csv)
		csv_zip.writestr("9-Dadus_Ekipamentu.csv", dataset9.csv)
		csv_zip.writestr("10-Dadus_KuantidadeEkipamentu.csv", dataset10.csv)
		csv_zip.writestr("11-Dadus_DetalluEkipamentu.csv", dataset11.csv)
		csv_zip.writestr("12-Dadus_Utilizador.csv", dataset12.csv)
		csv_zip.writestr("13-Dadus_UtilizaEkipamentu.csv", dataset13.csv)
		csv_zip.writestr("14-Dadus_LabInventory.csv", dataset14.csv)
		csv_zip.writestr("15-Dadus_LabInventoryStock.csv", dataset15.csv)
		csv_zip.writestr("16-Dadus_LabInventoryTransaction.csv", dataset16.csv)

	return redirect('home')
	

	



