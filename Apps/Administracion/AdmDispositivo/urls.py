from django.urls import include, path

from Apps.Administracion.AdmDispositivo.Views.AdmDispositivoView import AbrirDispositivoView, CerrarDispositivoView, CrearDispositivoView


 
urlpatterns = [
    path('crear',CrearDispositivoView.as_view(),name ='Metodo que crea un dispositivo'),
    path('abrir',AbrirDispositivoView.as_view(),name ='Metodo que abre el dispositivo'),
    path('cerrar',CerrarDispositivoView.as_view(),name ='Metodo que cierra un dispositivo'),
    
]