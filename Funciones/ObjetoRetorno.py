def retorno(status , estado:int , mensaje:str, data=None,totalRegistros= None):
    return {
        'status' : status ,
        'estado': estado,
        'mensaje':mensaje,
        'datos':data , 
        'total_registros': totalRegistros 
    }