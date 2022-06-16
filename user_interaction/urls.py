from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('slogin/', views.sloginPage),
    path('sregister/', views.sregister),
    path('rlogin/', views.rloginPage),
    path('rregister/', views.rregister),
    path('studentProfile/', views.studentProfile),
    path('studentProfileUpdate/', views.studentProfileUpdate),
    path('recruiterProfile/', views.recruiterProfile),
    path('job/', views.job),
    path('jobEdit/', views.jobEdit),
    path('studentSearch/', views.studentSearch),
    path('studentView/', views.studentView),
    path('jobSearch/', views.jobSearch),
    path('jobView/', views.jobView),
    path('sotp/', views.sotp),
    path('rotp/', views.rotp)
]
