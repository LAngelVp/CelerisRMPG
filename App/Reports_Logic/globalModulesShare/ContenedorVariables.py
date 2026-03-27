"""
DESARROLLADOR
LUIS A. PEREZ
"""
import json
import os
from datetime import *
from webbrowser import *
import calendar
import pandas as pd
import locale
from dateutil import parser
from openpyxl import *
import xlrd

from .documentos_json import creacion_json
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Variables:
    def __init__(self):
        self.fecha_hoy = datetime.now()
        self.FechaHoy = f'{self.fecha_hoy.day}/{self.fecha_hoy.month}/{self.fecha_hoy.year}'
        self.fechaInsertar = datetime.strptime(self.FechaHoy, "%d/%m/%Y")
        self.separador = os.sep
        self.folder_global = 'ProcessRMPG73'
        self.folder_name_kwrb = 'RMPG_ConcesionarioKenworthRioBravo'
        self.folder_name_kwe = 'RMPG_ConcesionarioKenworthdelEste'
        self.folder_name_kwkrei = 'RMPG_ConcesionarioKREI'
        self.folder_name_kwsonora = 'RMPG_ConcesionarioKenworthSonora'
        self.documentos_Trabajos = "Trabajos"
        self.documentos_originales = "Original"
        self.documentos_Errores = "Errores"
        self.documentos_Procesados = "Exitosos"
        self.help_documents_directory = "HelpDocumetsPrivate"

        self.customer_payment_goals_file = 'CustomerPaymentGoals.json'
        self.document_saving_paths_file = 'DocumentSavingPaths.json'
        self.movement_date_document_file = 'DateMovemment.json'
        self.vendor_service_departments_file = 'Vendedores_servicio_departamentos.json'
        self.clasificacion_vendedores_servicio_sonora = 'Clasificacion_vendedores_servicio_sonora.json'
        self.vendor_parts_departments_file = 'Vendedores_refacciones_departamentos.json'
        self.clasificacion_vendedores_refacciones_sonora = "Clasificacion_vendedores_refacciones_sonora.json"
        self.large_clients_parts_file = 'clientes_grandes.json'
        self.parts_brands_file = 'marcas_refacciones.json'
        self.departamentos_vendedores_ventas_perdidas = "vendedores_ventas_perdidas.json"
        self.coordenadas_financiero = "coordenadas_financiero.json"
        self.clientes_financiero = "clientes_financiero.json"
        documentoDatosVersionVp = "DataVersionVp.json"

        self.root_directory_system = os.path.expanduser(f'~{self.separador}')
        self.global_route_project = os.path.join(self.root_directory_system, self.folder_global).replace('\\','/')
        self.route_kwrb = os.path.join(self.global_route_project, self.folder_name_kwrb).replace('\\','/')
        self.route_kwe = os.path.join(self.global_route_project, self.folder_name_kwe).replace('\\','/')
        self.route_kwkrei = os.path.join(self.global_route_project, self.folder_name_kwkrei).replace('\\','/')
        self.route_kwsonora = os.path.join(self.global_route_project, self.folder_name_kwsonora).replace('\\','/')
        self.ruta_Trabajos_kwrb = os.path.join(self.route_kwrb, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwrb = os.path.join(self.route_kwrb, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwrb = os.path.join(self.route_kwrb, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwrb = os.path.join(self.route_kwrb, self.documentos_Procesados).replace('\\','/')

        self.ruta_Trabajos_kwe = os.path.join(self.route_kwe, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwe = os.path.join(self.route_kwe, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwe = os.path.join(self.route_kwe, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwe = os.path.join(self.route_kwe, self.documentos_Procesados).replace('\\','/')

        self.ruta_Trabajos_krei = os.path.join(self.route_kwkrei, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_krei = os.path.join(self.route_kwkrei, self.documentos_originales).replace('\\','/')
        self.ruta_errores_krei = os.path.join(self.route_kwkrei, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_krei = os.path.join(self.route_kwkrei, self.documentos_Procesados).replace('\\','/')
        self.ruta_Trabajos_kwsonora = os.path.join(self.route_kwsonora, self.documentos_Trabajos).replace('\\','/')
        self.ruta_original_kwsonora = os.path.join(self.route_kwsonora, self.documentos_originales).replace('\\','/')
        self.ruta_errores_kwsonora = os.path.join(self.route_kwsonora, self.documentos_Errores).replace('\\','/')
        self.ruta_exitosos_kwsonora = os.path.join(self.route_kwsonora, self.documentos_Procesados).replace('\\','/')
        self.help_directory = os.path.join(self.global_route_project, self.help_documents_directory).replace('\\','/')
        self.rutaDatosVersionVp = os.path.join(self.help_directory, documentoDatosVersionVp).replace('\\', '/')
        self.customerPaymentGoals = os.path.join(self.help_directory, self.customer_payment_goals_file).replace('\\','/')
        self.documentSavingPaths = os.path.join(self.help_directory, self.document_saving_paths_file).replace('\\','/')
        self.movement_date_document = os.path.join(self.help_directory,  self.movement_date_document_file).replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_servicio_kwe = os.path.join(self.help_directory, self.vendor_service_departments_file).replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_servicio_sonora = os.path.join(self.help_directory, self.clasificacion_vendedores_servicio_sonora).replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_refacciones_kwe = os.path.join(self.help_directory, self.vendor_parts_departments_file).replace('\\','/')
        self.nombre_documento_clasificacion_vendedores_refacciones_sonora = os.path.join(self.help_directory, self.clasificacion_vendedores_refacciones_sonora).replace('\\','/')
        self.tamaño_clientes_refacciones_kwe = os.path.join(self.help_directory, self.large_clients_parts_file).replace('\\','/')
        self.marcas_refacciones_kwe = os.path.join(self.help_directory, self.parts_brands_file).replace('\\','/')

        self.successfulPathDirectory = {
            "KWRB" : self.ruta_exitosos_kwrb,
            "KWESTE" : self.ruta_exitosos_kwe,
            "KWKREI" : self.ruta_exitosos_krei,
            "KWSON" : self.ruta_exitosos_kwsonora,
        }

        self.pdf = 'https://docs.google.com/document/d/1-TeaeWdGAXUGls18b_hH6qG-Ur1PqDznsWS8X9FPD_M/edit?usp=sharing' #NOTE Direccion en donde se encuentra el archivo de apoyo

    def create_root_directory(self):
        try:
            if not os.path.exists(self.global_route_project):
                os.mkdir(self.global_route_project)
                
            else:
                print("La ruta raiz existe")
        except:
            pass
        return self.global_route_project

    def date_movement_config_document(self):
        document = pd.read_json(self.movement_date_document)
        date_movement = parser.parse(document.iloc[0]["fecha_movimiento"]) 
        return date_movement

    def comprobar_reporte_documento_rutas(self, nombre = None, concesionario = None):
        almacenamiento_csv = None
        almacenamiento_excel = None
        nombre_base = nombre.split(".")[0]
        archivo = pd.read_json(self.documentSavingPaths)
        nombre_arreglado_csv = f'{concesionario}_{nombre_base}_RMPG_{self.FechaExternsionGuardar()}.csv'
        nombre_arreglado_xlsx = f'{concesionario}_{nombre_base}_RMPG_{self.FechaExternsionGuardar()}.xlsx'
        
        self.docu =None
        self.docu_nombre = None
        for index, fila in archivo.iterrows():
            nombre_fila_base = fila["nombre"].split(".")[0]
            if nombre_fila_base == nombre_base:
                self.docu_nombre = fila["nombre"]
                self.docu = str(fila["path"])
                break
        if (self.docu is not None) | (self.docu_nombre == nombre):
            almacenamiento_csv = os.path.join(self.docu,nombre_arreglado_csv)
        else:
            if (concesionario in self.successfulPathDirectory):
                almacenamiento_excel = os.path.join(self.successfulPathDirectory[concesionario],nombre_arreglado_xlsx)
                return almacenamiento_csv, almacenamiento_excel
            
        if (concesionario in self.successfulPathDirectory):
                almacenamiento_excel = os.path.join(self.successfulPathDirectory[concesionario],nombre_arreglado_xlsx)
        return almacenamiento_csv, almacenamiento_excel
    def guardar_datos_dataframe(self, nombre_documento, dataframe, concesionario = None):
        ruta_csv, ruta_excel= (self.comprobar_reporte_documento_rutas(nombre_documento, concesionario))
        if ruta_csv is None:
            extension_documento_ruta_devuelta = os.path.basename(ruta_excel).split(".")[1]
        else:
            extension_documento_ruta_devuelta = os.path.basename(ruta_csv).split(".")[1]
        extencion_documento_insertado = nombre_documento.split(".")[1]
        if (extension_documento_ruta_devuelta == extencion_documento_insertado):
                dataframe.to_excel(ruta_excel, index=False )
        else:
            dataframe.to_csv(ruta_csv, encoding="utf-8-sig", index=False)
            dataframe.to_excel(ruta_excel, index=False)
            
    def guardar_xls(self, nombre_documento, dataframe, concesionario = None):
        ruta_devuelta_csv, ruta_devuelta_excel = self.comprobar_reporte_documento_rutas(nombre_documento, concesionario)
        
        if ruta_devuelta_csv is not None:
            if ruta_devuelta_csv.endswith('.csv'):
                dataframe.to_csv(ruta_devuelta_csv, encoding="utf-8-sig", index=False)
                dataframe.to_excel(ruta_devuelta_excel, index=False, engine='openpyxl')
                print(f"Guardado como CSV: {ruta_devuelta_csv}")
        elif ruta_devuelta_excel is not None:
            dataframe.to_excel(ruta_devuelta_excel, index=False, engine='openpyxl')
            print(f"Guardado como XLSX: {ruta_devuelta_excel}")
    def FechaExternsionGuardar(self):
        datoAdicional = datetime.now()
        fechaPath = datoAdicional.strftime('%d-%m-%Y-%H-%M-%S') #NOTE Fecha para adicionar al nombre del archivo procesado.
        return fechaPath
    
    def nombre_mes(self):
        mes_actual = self.date_movement_config_document().month
        mes_actual_nombre = calendar.month_name[mes_actual].capitalize()
        return mes_actual_nombre
    
    def year_completo(self):
        year_actual = self.date_movement_config_document().year
        return year_actual
    
    def nombre_mes_actual_abreviado(self):
        mes_actual = self.date_movement_config_document()
        mes_abreviado = mes_actual.strftime(f'%b-%y').replace(".","").lower()
        return mes_abreviado
    
    def fechaHoy(self):
        fecha = datetime.now()
        return fecha
    
    def nombre_mes_base_columna(self, valor):
        mes = valor.strftime(f'%b-%y').replace(".","").lower()
        return mes
    
    def nombre_mes_completo_base_columna(self, valor):
        mes = valor.strftime(f'%B').replace(".","").capitalize()
        return mes
    
    def nombre_año_completo_base_columna(self, valor):
        año = valor.strftime(f'%Y').replace(".","")
        return año
    
    # def parse_date_safe(self, date_str):
    #     try:
    #         parsed_date = parser.parse(date_str, dayfirst=True)
    #         if parsed_date:
    #             date_only = parsed_date.date()
    #             datetime_with_midnight = parser.parse(str(date_only))
    #             return datetime_with_midnight
    #         else:
    #             return None
    #     except (parser.ParserError, TypeError, ValueError):
    #         return None
        
    # def global_date_format_america(self, data, name_column=None):
    #     if name_column in data.columns:
    #         if pd.api.types.is_datetime64_any_dtype(data[name_column]):
    #             try:
    #                 data[name_column] = pd.to_datetime(data[name_column]).dt.date
    #                 data[name_column] = pd.to_datetime(data[name_column], dayfirst=True)
    #             except:
    #                 pass
    #         elif pd.api.types.is_object_dtype(data[name_column]):
    #                 data[name_column] = data[name_column].astype(str)
    #                 data[name_column] = data[name_column].apply(self.parse_date_safe)
    #         else:
    #             pass
    #     return data
    
    # def global_date_format_mdy_america(self, data, name_column=None):
    #     if name_column in data.columns:
    #         if pd.api.types.is_datetime64_any_dtype(data[name_column]) or pd.api.types.is_object_dtype(data[name_column]):
    #             data[name_column] = data[name_column].apply(lambda x: x.strftime("%m/%d/%Y") if not pd.isnull(x) else pd.NaT)
    #         else:
    #             pass
    #     return data
    
    # def global_date_format_dmy_mexican(self, data, name_column=None):
    #     if name_column in data.columns:
    #         if pd.api.types.is_datetime64_any_dtype(data[name_column]) or pd.api.types.is_object_dtype(data[name_column]):
    #             data[name_column] = data[name_column].apply(lambda x: x.strftime("%d/%m/%Y") if not pd.isnull(x) else pd.NaT)
    #         else:
    #             pass
    #     return data

    def parse_date_safe(self, date_str):
    # Simplificado: to_datetime es más robusto y rápido que parser.parse manual
        try:
            return pd.to_datetime(date_str, dayfirst=True, errors='coerce')
        except:
            return None

    def global_date_format_america(self, data, name_column=None):
        if name_column in data.columns:
            # Convertimos a datetime real y normalizamos (quita horas/minutos/segundos)
            # errors='coerce' reemplaza los errores por NaT (equivalente a tu None)
            data[name_column] = pd.to_datetime(data[name_column], dayfirst=True, errors='coerce').dt.normalize()
        return data

    def global_date_format_mdy_america(self, data, name_column=None):
        if name_column in data.columns:
            # Usamos .dt.strftime que es 10 veces más rápido que .apply(lambda...)
            # Solo funciona si la columna es tipo datetime (por eso el paso anterior es vital)
            if pd.api.types.is_datetime64_any_dtype(data[name_column]):
                data[name_column] = data[name_column].dt.strftime("%m/%d/%Y")
        return data

    def global_date_format_dmy_mexican(self, data, name_column=None):
        if name_column in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[name_column]):
                data[name_column] = data[name_column].dt.strftime("%d/%m/%Y")
        return data

    def clasificacion_vendedores_departamentos_refacciones(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_refacciones_kwe)
        return documento
    def clasificacion_vendedores_departamentos_refacciones_sonora(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_refacciones_sonora)
        return documento
    def clasificacion_tamaño_clientes_refacciones(self):
        documento = pd.read_json(self.tamaño_clientes_refacciones_kwe)
        return documento
    def marcas_refacciones_fun(self):
        documento = pd.read_json(self.marcas_refacciones_kwe)
        return documento
    def vendedores_y_depas_este_servicio(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_servicio_kwe)
        return documento
    def vendedores_y_depas_este_servicio_sonora(self):
        documento = pd.read_json(self.nombre_documento_clasificacion_vendedores_servicio_sonora)
        return documento
    
    def actualizar_fecha_movimiento(self):
        fecha_actual = datetime.today().date()
        objeto_fecha_movimiento = {
            "fecha_movimiento" : str(fecha_actual)
        }
        if os.path.exists(os.path.join(self.help_directory,self.movement_date_document_file)):
            self.colocar_fecha_actual(fecha_actual)
        else:
            creacion_json(self.help_directory,self.movement_date_document_file).comprobar_existencia
            creacion_json(self.help_directory,self.movement_date_document_file, objeto_fecha_movimiento).agregar_json

    def colocar_fecha_actual(self, nueva_fecha):
        fecha_antigua = creacion_json(self.help_directory,self.movement_date_document_file).comprobar_existencia
        id_fecha = fecha_antigua[0]['id']
        id = {"id" : str(id_fecha)}
        nueva_fecha_tipada = nueva_fecha
        nuevo_objeto_fecha = {
            'id' : id['id'],
            'fecha_movimiento' : str(nueva_fecha_tipada)
        }
        creacion_json(self.help_directory,self.movement_date_document_file,id).actualizar_datos(nuevo_objeto_fecha)