import traceback
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
import xlrd
import locale
from time import sleep

class VentasPerdidas(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        self.df_final = pd.DataFrame()
        self.documentos_ventasperdidas_sucursal = [
            {"archivo" : "VPNLM.xls", "sucursal" : "NUEVO LAREDO (MATRIZ)"},
            {"archivo" : "VPR.xls", "sucursal" : "REYNOSA"},
            {"archivo" : "VPM.xls", "sucursal" : "MATAMOROS"},
            {"archivo" : "VPPN.xls", "sucursal" : "PIEDRAS NEGRAS"},
            {"archivo" : "VPNLA.xls", "sucursal" : "NUEVO LAREDO (AEROPUERTO)"},
            {"archivo" : "VPPR.xls", "sucursal" : "POZA RICA"},
            {"archivo" : "VPVH.xls", "sucursal" : "VALLE HERMOSO"},
            {"archivo" : "VPTRPN.xls", "sucursal" : "TRP NAVA"},
            {"archivo" : "VPTRPR.xls", "sucursal" : "TRP REYNOSA"},
            {"archivo" : "VPTRPNL.xls", "sucursal" : "TRP NUEVO LAREDO"},
            {"archivo" : "VPTRPA.xls", "sucursal" : "TRP ACUÑA"},
        ]
        
        # Asegúrate de que 'ruta_ventasperdidas' sea una propiedad de la clase
        self.ruta_ventasperdidas = None
        # Obtener la ruta base donde se almacenan los archivos
        self.ruta_base = self.variables.ruta_Trabajos_kwrb
            
    def venta_perdida_nuevo_laredo_matriz(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPNLM.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def venta_perdida_reynosa(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPR.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def venta_perdida_matamoros(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPM.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def venta_perdida_piedras_negras(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPPN.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def venta_perdida_nuevo_laredo_aeropuerto(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPNLA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def venta_perdida_poza_rica(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPPR.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()

    def venta_perdida_valle_hermoso(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPVH.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()

    def venta_perdida_trp_nava(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTRPN.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()

    def venta_perdida_trp_reynosa(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTRPR.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()

    def venta_perdida_trp_nuevo_laredo(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTRPNL.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()

    def venta_perdida_trp_acuña(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTRPA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
# comment: funciones
    def proceso(self, nombre_documento):
        self.nombre_doc = nombre_documento
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)

        # Leer el archivo Excel
        df = pd.read_excel(path, sheet_name=0)

        if df.empty:
            # Buscar la sucursal correspondiente
            sucursal = next((item["sucursal"] for item in self.documentos_ventasperdidas_sucursal if item["archivo"] == nombre_documento), None)
            if sucursal:
                print(f"El archivo {nombre_documento} está vacío. Se generará fila en cero para la sucursal: {sucursal}")
                fila_en_cero = self.creacion_filas_en_cero(documento_con_contenido = False, sucursal = sucursal, refacciones = "Refacciones")
                return fila_en_cero, True
        # Reemplazar los puntos y comas por guiones
        df = df.replace(to_replace=";", value="-", regex=True)
        df = df.drop(df.index[-1])  # Eliminar la última fila
        df.drop(["Hora"], axis=1, inplace=True)

        # Procesar las columnas de fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)

        df["Mes"] = df["Fecha"].apply(lambda x:self.variables.nombre_mes_completo_base_columna(x))
        
        df["Año"] = df["Fecha"].apply(lambda x:self.variables.nombre_año_completo_base_columna(x))
        
        df.insert(0, "VP", 1, allow_duplicates=False)

        # Concatenar la columna "Venta Perdida"
        col_venta_perdida_concat = "VP-" + df["Venta Perdida"].astype(int).astype(str)
        df["Venta Perdida"] = col_venta_perdida_concat

        # Mapear los departamentos
        df.insert(loc=11,column="Departamento", value="Refacciones", allow_duplicates=False)

        # Reconvertir las fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_dmy_mexican(df, column_name)

        # Convertir columnas booleanas a texto
        columnas_bol = df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        return df, False  # Devolver el DataFrame procesado

    def comprobar_documento(self, documento):
        ruta_completa = os.path.join(self.ruta_base, documento)
        if not os.path.exists(ruta_completa):
            print(f"El documento {documento} no existe")
            return

        df, es_fila_en_cero = self.proceso(documento)

        if df is None or df.empty:
            return

        sucursal = df["Sucursal"].iloc[0]

        # Eliminar fila en cero si existe para esta sucursal
        if self.df_final is not None:
            self.df_final = self.df_final[~((self.df_final["Sucursal"] == sucursal) & (self.df_final["VP"] == 0))]

        # Agregar nuevos datos procesados
        self.df_final = pd.concat([self.df_final, df], ignore_index=True)
        print(f"Documento procesado y agregado: {documento}")
        
    def comprobar_existencia_ventasperdidas(self):
         # Buscar si ya existe un archivo con ventas perdidas
        self.df_final = None
        for archivo in os.listdir(self.variables.ruta_exitosos_kwrb):
            if "ventasperdidas" in archivo:
                self.ruta_ventasperdidas = os.path.join(self.variables.ruta_exitosos_kwrb, archivo)

        # Si ya existe, lo carga
        if self.ruta_ventasperdidas and os.path.exists(self.ruta_ventasperdidas):
            self.df_final = pd.read_excel(self.ruta_ventasperdidas)
            print("Archivo encontrado y abierto")
        else:
            # Si no existe, crear filas en cero para todas las sucursales
            df_filas_cero = []
            for item in self.documentos_ventasperdidas_sucursal:
                sucursal = item["sucursal"]
                fila = self.creacion_filas_en_cero(documento_con_contenido=False, sucursal=sucursal)
                df_filas_cero.append(fila)
            self.df_final = pd.concat(df_filas_cero, ignore_index=True)
        print("Se crearon filas en cero para todas las sucursales")
            
    def creacion_filas_en_cero(self, documento_con_contenido, sucursal, refacciones = None):
        def crear_fila(departamento):
            fecha = Variables().date_movement_config_document()
            return pd.DataFrame({
                "VP": [0],
                "Venta Perdida": ["-"],
                "Id. Cliente": [0],
                "Nombre Cliente": ["-"],
                "Núm. Artículo": ["-"],
                "Artículo": ["-"],
                "Motivo": ["NO EXIST EN SUCURSAL (MOVTO)"],
                "Cantidad": [0],
                "Fecha": [fecha],
                "Hora": [fecha],
                "Comentario": ["-"],
                "Usuario": ["-"],
                "Departamento": [departamento],
                "Sucursal": [sucursal],
                "Programa": ["Ventas Perdidas"],
                "Tipo de Inventario": ["Refacciones"],
                "Precio": [0],
                "Clasificación": ["E"],
                "Desc. Clasificación": ["Sin Eventos"],
                "Costo": [0],
                "Total": [0],
                "Id. Competidor": [0],
                "Competidor": ["-"],
                "Precio Competidor": [0],
                "Moneda Competidor": ["-"]
            })

        dfs = []

        # Si 'servicio' no es None, crear la fila de "Refacciones"
        fila_refacciones = crear_fila("Refacciones")
        dfs.append(fila_refacciones)

        # Si se generaron filas, concatenarlas y devolver el resultado
        if dfs:
            fila_dataframe = pd.concat(dfs, ignore_index=True)
            fila_dataframe["Mes"] = fila_dataframe["Fecha"].apply(lambda x:self.variables.nombre_mes_completo_base_columna(x))
            fila_dataframe["Año"] = fila_dataframe["Fecha"].apply(lambda x:self.variables.nombre_año_completo_base_columna(x))
            hora = pd.to_datetime(fila_dataframe["Hora"])
            fila_dataframe["Hora"] = hora.dt.strftime('%I:%M:%S %p').astype(str)
            for column_name in fila_dataframe.columns:
                if "fecha" in column_name.lower():
                    fila_dataframe = self.variables.global_date_format_dmy_mexican(fila_dataframe, column_name)
            return fila_dataframe

        return pd.DataFrame()  # Si no se generaron filas, devolver un DataFrame vacío
    
    def guardar_todo(self):
        if not self.df_final.empty:
            self.variables.guardar_xls("ventasperdidas.xls", self.df_final, self.concesionario)
            print("Archivo final de ventas perdidas guardado correctamente.")
        else:
            print("No hay datos para guardar.")