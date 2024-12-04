import time
import jwt 
import  Base.settings
def crea_token_jwt(datos):
    return jwt.encode(datos, Base.settings.SECRET_KEY)
    
def valida_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    datos={}
    if token is None:
        datos['mensaje']='Token no disponible'
        return datos
    token = token.split('Bearer ')[1]
    try:
        token_desencriptado = desencripta_token(token)
      # Verificar la expiración del token (opcional)
        # Si no deseas verificar la expiración, puedes omitir esta parte
       
        if 'exp' in token_desencriptado:
            exp_timestamp = token_desencriptado['exp']
            current_timestamp = int(time.time())
            if current_timestamp > exp_timestamp:
                datos['mensaje']='Token expiró'
                

            # El token es válido
            else:   
                datos= token_desencriptado
                datos['mensaje']= 'valido'
            
    except jwt.ExpiredSignatureError:
    # Captura el error y devuelve una respuesta JSON personalizada
         datos['mensaje']= "El token ha expirado. Por favor, inicie sesión nuevamente."
            
    except jwt.InvalidTokenError:
         datos['mensaje']= "Token inválido."

    except Exception as a:
        # El token no es válido
        datos['mensaje']=a
   
    
    return datos 
    
    
def desencripta_token(token):
    return jwt.decode(token, Base.settings.SECRET_KEY,algorithms='HS256')