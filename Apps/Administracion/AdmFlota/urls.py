from django.urls import include, path

from Apps.Administracion.AdmFlota.Views.AdmFlotaView import ListaFlotasView


 
urlpatterns = [
    path('lista_por_clientes',ListaFlotasView.as_view(),name ='Metodo que lista flotas por cliente')
]