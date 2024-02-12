from django.urls import path
from . import views
urlpatterns = [
	path('badge/used/total/', views.APINotifBadge.as_view()),
	path('badge/used/deadline/total/', views.APINotifBadgeDeadline.as_view()),
	path('badge/used/deadline-aban/total/', views.APINotifBadgeDeadlineAban.as_view()),
]