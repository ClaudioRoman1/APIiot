from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno


class  TestView(generics.ListAPIView):
    """Metodo que muestra la lista de regiones por países
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    def get(self,request):
            return Response(data='Activo')
        