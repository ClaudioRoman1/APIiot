
from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmPais.Models.AdmPaisModel import AdmPais
from Apps.Administracion.AdmPais.Serializers.AdmPaisSerializer import ListaPaisesSerializer
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from Apps.RestBase.Constantes import MensajeRetornos

# Create your views here.
"""Funcion que lista países
    Retorno : retorno
    Remarks: CRoman 2023-05-22"""
class ListaPaisesView(generics.ListAPIView):
    def get(self,request):
            paises = AdmPais.objects.obtener_todos()
            ls_resultado = list(paises)
            total_reg=len(ls_resultado) 
            if total_reg==0:
                return Response(retorno(status.HTTP_200_OK, 0,MensajeRetornos.mensajeBusquedaOkSr ))
            
            lista_paises = ListaPaisesSerializer(instance=paises,many=True)
            
            return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeBusquedaOk, lista_paises.data, total_reg ))
    
    