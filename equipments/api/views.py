import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import Municipality
from users.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from equipments.models import *
from datetime import datetime, timedelta
from custom.utils import *



# @login_required
# @allowed_users(allowed_roles=['Administracao Laboratorio','Admin','Cordenador Laboratorio','Director','Vice Director'])
class APINotifBadge(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		obj1 = UtilizaEkipamentu.objects.filter(data_atu_entrega__lte=datetime.now(),is_return=False,item__status = 'Uza Hela').all().count()
		obj2 = UtilizaEkipamentu.objects.filter(data_atu_entrega=datetime.now() + timedelta(days=1),is_return=False,item__status='Uza Hela').all().count()
		objects = obj1 + obj2
		return Response({'value':objects})

class APINotifBadgeDeadline(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		obj1 = UtilizaEkipamentu.objects.filter(data_atu_entrega__lte=datetime.now(),is_return=False,item__status = 'Uza Hela').all().count()
		objects = obj1
		return Response({'value':objects})

class APINotifBadgeDeadlineAban(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		obj2 = UtilizaEkipamentu.objects.filter(data_atu_entrega=datetime.now() + timedelta(days=1),is_return=False,item__status='Uza Hela').all().count()
		objects = obj2
		return Response({'value':objects})
