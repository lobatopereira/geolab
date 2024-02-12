from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import *


@login_required
def home(request):
	context = {
		"title":"VARANDA",
		"legend":"VARANDA",
	}
	return render(request, 'main/index.html', context)

# from ipware import get_client_ip
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			AuditLogin.objects.create(user=request.user)
			return redirect('home')
		else:
			messages.error(request,'Username ou Password la loos! Favor Prense fali!')
	context = {
		"title":"Pajina Login",
	}
	return render(request,'auth/login.html',context)

def error_404(request, exception):
    data = {}
    return render(request,'auth/404.html', data)

def error_500(request):
    data = {}
    return render(request,'auth/500.html', data)