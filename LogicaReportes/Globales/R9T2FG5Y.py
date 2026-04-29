import requests
import csv
from datetime import datetime
URL_CSV = "https://docs.google.com/spreadsheets/d/1MaBvEeh8FX585CO9FlImGJSpxs6PwNzlb-EQSdNbYNk/export?format=csv"

def verificar_acceso(usuario_ingresado, password_ingresada):
    fecha_actual = datetime.now().date()
    try:
        response = requests.get(URL_CSV)
        response.raise_for_status()
        response.encoding = 'utf-8-sig'
        contenido = response.text.splitlines()
        lector = csv.reader(contenido)
        next(lector)
        for fila in lector:
            user_excel = fila[0]
            pass_excel = fila[1]
            licencia_str = fila[2]
            if user_excel == usuario_ingresado and pass_excel == password_ingresada:
                fecha_licencia = datetime.strptime(licencia_str, '%Y-%m-%d').date()
                if fecha_actual < fecha_licencia:
                    return {
                        'estado':True, 
                        'mensaje':'Usuario logueado exitosamente',
                        'disponible':True,
                        'fecha_actual':fecha_actual,
                        'fecha_fin_licencia':fecha_licencia
                        }
                else:
                    return {
                        'estado':True,
                        'mensaje':'Licencia expirada',
                        'disponible':False,
                        'fecha_actual':fecha_actual,
                        'fecha_fin_licencia':fecha_licencia
                        }
        return {'estado':False, 
            'mensaje':'Error en la validación, usuario o contraseña incorrectos.',
            'disponible':True,
            'fecha_actual':fecha_actual,
            'fecha_fin_licencia':None}
    except requests.exceptions.ConnectionError:
        mensaje = "ERROR DE CONEXIÓN: No se pudo conectar al servidor. Revisa tu internet."
        return {
            'estado':False, 
            'mensaje':mensaje,
            'disponible':True,
            'fecha_actual':fecha_actual,
            'fecha_fin_licencia':None
            }
    except requests.exceptions.Timeout:
        mensaje ="ERROR: La solicitud tardó demasiado tiempo (Timeout)."
        return {
            'estado':False, 
            'mensaje':mensaje,
            'disponible':True,
            'fecha_actual':fecha_actual,
            'fecha_fin_licencia':None
            }
    except Exception as e:
        mensaje = f"ERROR INESPERADO: {e}"
        return {
            'estado':False, 
            'mensaje':mensaje,
            'disponible':True,
            'fecha_actual':fecha_actual,
            'fecha_fin_licencia':None}
