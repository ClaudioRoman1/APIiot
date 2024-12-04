from django.urls import path

from Apps.Administracion.AdmTest.AdmTestView.AdmTestView import TestView 



 
urlpatterns = [
    path('',TestView.as_view(),name ='Test para dispositivo'),
]