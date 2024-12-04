from django.urls import include, path

from Apps.Administracion.AdmRegion.Views.AdmRegionView import ListaRegionesView

 
urlpatterns = [
    path('lista_regiones_por_paises',ListaRegionesView.as_view(),name ='Metodo que lista regiones por países')
]