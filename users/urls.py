from django.urls import path
from . import views
urlpatterns = [

	##############
	path('profile/', views.ProfileUpdate, name="user-profile"),
	path('my/account/', views.AccountUpdate, name='user-account'),
	path('my/account/login/history/', views.AccountLoginHistory, name='user-login-history'),
	path('change/password/', views.UserPasswordChangeView.as_view(), name='user-change-password'),
	path('change/password/done/', views.UserPasswordChangeDoneView.as_view(), name='user-change-password-done'),
	

	path('list/', views.UserList, name="userlist"),
	path('create/', views.createUser, name="createUser"),
	path('ativu-user/<str:id>', views.ativuUser, name="ativuUser"),
	path('desativu-user/<str:id>', views.desativuUser, name="desativuUser"),
	path('reset-user-password/<str:id>', views.resetUserPassword, name="resetUserPassword"),
	
	path('list/group/<str:id>', views.user_with_group, name="user_with_group"),
	
	path('backup/geolab', views.BackupDadusGEOLAB, name="BackupDadusGEOLAB"),

]