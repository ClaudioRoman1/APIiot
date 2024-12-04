from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmRegion.Models.AdmRegionModel import AdmRegion
from Apps.Administracion.AdmRegion.Serializers.AdmRegionSerializer import ListaRegionesSerializer
from Funciones.ObjetoRetorno import retorno
class  ListaRegionesView(generics.ListAPIView):
    """Metodo que muestra la lista de regiones por países
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    
    def post(self,request):
        id_pais = request.data.get('id_pais')
        datos = {
            'id_pais':id_pais
        }
        serializer = ListaRegionesSerializer(data=datos)
        if serializer.is_valid():
            regiones = AdmRegion.objects.por_pais(ipaisid = id_pais)
            ls_regiones = list(regiones)
            
            if len(ls_regiones) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No se encuentran regiones para este país', None,None))
        
            lista_regiones = ListaRegionesSerializer(instance=regiones,many=True)
            lista_regiones_serializadas= lista_regiones.data 
            total_reg = len(lista_regiones_serializadas)
        
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_regiones_serializadas, total_reg ))
        


