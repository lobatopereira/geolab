from django.shortcuts import render, redirect, get_object_or_404
# import numpy as np
from django.db.models import Count, Q
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User, Group
import datetime
from equipments.models import *
from reports.utils import getFulanNaran
from datetime import date


class APIGEquipmentStatusSumm(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		# totalEkipamentu = DetalluEkipamentu.objects.all().count()
		ekipamentuUzaHela = DetalluEkipamentu.objects.filter(status='Uza Hela').count()
		ekipamentuDisponivel = DetalluEkipamentu.objects.filter(status='Disponivel').count()
		ekipamentuDiak = DetalluEkipamentu.objects.filter(kondisaun='Diak').count()
		ekipamentuAat = DetalluEkipamentu.objects.filter(kondisaun='Aat').count()
		label = ["Ekipamentu Uza Hela","Ekipamentu Disponivel"]
		obj = [ekipamentuUzaHela,ekipamentuDisponivel]
		data = { 'label': label, 'obj': obj }
		return Response(data)

class APIGEquipmentKondisaunSumm(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		ekipamentuDiak = DetalluEkipamentu.objects.filter(kondisaun='Diak').count()
		ekipamentuAat = DetalluEkipamentu.objects.filter(kondisaun='Aat').count()
		label = ["Ekipamentu Diak","Ekipamentu Aat"]
		obj = [ekipamentuDiak,ekipamentuAat]
		data = { 'label': label, 'obj': obj }
		return Response(data)

class APIGEquipmentTamaFulanTinanAtual(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		listaDoador = Doadores.objects.all()
		monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
		for x in listaDoador:
			labels.append(x.kodigu)
		for x in monthListOrder:
			obj_c_f_ass = []
			for i in listaDoador:
				ekipamentu = DetalluEkipamentu.objects.filter(ekipamentu__doador__id=i.id,ekipamentu__data_simu__month=x,ekipamentu__data_simu__year=date.today().year).count()
				if ekipamentu == None:
					ekipamentu = 0
				else:
					ekipamentu = ekipamentu
				obj_c_f_ass.append(ekipamentu)
			label.append(getFulanNaran(x))
			obj.append(obj_c_f_ass)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGInventariatuirFulanTinanAtual(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
		labels = ["Total Tama","Total Sai"]
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
			label.append(getFulanNaran(x))
			obj.append([totaltama,totalsai])
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGEquipmentTamaTuirTinan(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		years = DetalluEkipamentu.objects.distinct().values('ekipamentu__data_simu__year').all().order_by('ekipamentu__data_simu__year')
		for x in years:
			totalEkipamentuTinan = DetalluEkipamentu.objects.filter(ekipamentu__data_simu__year=x['ekipamentu__data_simu__year']).count()
			label.append(x['ekipamentu__data_simu__year'])
			obj.append(totalEkipamentuTinan)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGInventariaTuirTinan(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		labels = ["Total Tama","Total Sai"]
		years = LabInventoryTransaction.objects.distinct().values('data__year').all().order_by('data__year')
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
			label.append(x['data__year'])
			obj.append([totaltama,totalsai])
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)


class APIGSummKategoria(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj = list(),list()
		listaKategoria = Kategoria.objects.all()
		labels = ["Ekipamentu","Inventaria"]
		for x in listaKategoria:
			obj1 = DetalluEkipamentu.objects.filter(ekipamentu__kategoria__id=x.id).count()
			obj2 = LabInventoryStock.objects.filter(inventory__kategoria__id=x.id).aggregate(total_sum=Sum('total_stock'))['total_sum']
			if obj2:
				obj2 = obj2
			else:
				obj2 = 0

			label.append(x.kategoria)
			obj.append([obj1,obj2])
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGSummDoador(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj = list(),list()
		listaDoador = Doadores.objects.all()
		labels = ["Ekipamentu","Inventaria"]
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
			label.append(doador)
			obj.append([obj1,obj2])
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)