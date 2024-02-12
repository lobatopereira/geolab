from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from equipments.models import *

class DateInput(forms.DateInput):
	input_type = 'date'


class UtilizadorForm(forms.ModelForm):
	# date = forms.DateField(label='Data Produsaun', widget=DateInput())
	class Meta:
		model = Utilizador
		fields = ['naran','pozisaun','seksu','nu_kontaktu','image']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['naran'].required = True
		self.fields['seksu'].required = True
		self.fields['pozisaun'].required = True
		self.fields['nu_kontaktu'].required = True
		self.fields['image'].required = False
		self.fields['seksu'].widget.attrs.update({'class': 'form-control'})
		self.helper.layout = Layout(
			Row(
				Column('naran', css_class='form-group col-md-6 mb-0'),
				Column('seksu', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('pozisaun', css_class='form-group col-md-6 mb-0'),
				Column('nu_kontaktu', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('image', css_class='form-group col-md-6 mb-0', onchange="myFunction()"),
				css_class='form-row'
			),
			HTML(""" <center> <img id='output' width='200' /> </center> """),
			HTML(""" <div class="form-group text-left"><button class="btn btn-sm btn-info" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

class UtilizaEkipamentuForm(forms.ModelForm):
	data_empresta = forms.DateField(label='Data Empresta', widget=DateInput())
	data_atu_entrega = forms.DateField(label='Data Atu Entrega', widget=DateInput())
	class Meta:
		model = UtilizaEkipamentu
		fields = ['utilizador','data_empresta','data_atu_entrega']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['utilizador'].required = True
		self.fields['data_atu_entrega'].required = True
		self.fields['data_empresta'].required = True
		self.fields['utilizador'].widget.attrs.update({'class': 'form-control'})
		self.fields['data_atu_entrega'].widget.attrs.update({'class': 'form-control'})
		self.fields['data_empresta'].widget.attrs.update({'class': 'form-control'})
		
class UtilizadorEmprestaEkipamentuForm(forms.ModelForm):
	data_empresta = forms.DateField(label='Data Empresta', widget=DateInput())
	data_atu_entrega = forms.DateField(label='Data Atu Entrega', widget=DateInput())
	class Meta:
		model = UtilizaEkipamentu
		fields = ['item','data_empresta','data_atu_entrega']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['item'].queryset = DetalluEkipamentu.objects.filter(status='Disponivel',kondisaun='Diak')
		self.fields['item'].required = True
		self.fields['data_atu_entrega'].required = True
		self.fields['data_empresta'].required = True
		self.fields['item'].widget.attrs.update({'class': 'form-control'})
		self.fields['data_atu_entrega'].widget.attrs.update({'class': 'form-control'})
		self.fields['data_empresta'].widget.attrs.update({'class': 'form-control'})
		
class EntregaEkipamentuForm(forms.ModelForm):
	data_entrega = forms.DateField(label='Data Entrega', widget=DateInput())
	class Meta:
		model = UtilizaEkipamentu
		fields = ['kondisaun','data_entrega']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['kondisaun'].required = True
		self.fields['data_entrega'].required = True
		self.fields['kondisaun'].widget.attrs.update({'class': 'form-control'})
		self.fields['data_entrega'].widget.attrs.update({'class': 'form-control'})
		

class EquipmentSearchForm(forms.Form):
	search_query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control col-md-12', 'placeholder': 'Konsulta Ekipamentu. Naran Ekipamentu ka serial number'}),
        label=False
    )

class UtilizaInventoryForm(forms.ModelForm):
	data = forms.DateField(label='Data Foti', widget=DateInput())
	class Meta:
		model = LabInventoryTransaction
		fields = ['utilizador','data','total_sai']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['utilizador'].required = True
		self.fields['data'].required = True
		self.fields['total_sai'].required = True
		self.fields['utilizador'].widget.attrs.update({'class': 'form-control'})
		self.fields['data'].widget.attrs.update({'class': 'form-control'})
		self.fields['total_sai'].widget.attrs.update({'class': 'form-control'})
		