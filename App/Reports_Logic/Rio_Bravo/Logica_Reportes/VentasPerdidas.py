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

        self.documentos_ventasperdidas_sucursal = [
            "VPNLM.xls",
            "VPR.xls",
            "VPM.xls",
            "VPPN.xls",
            "VPNLA.xls",
            "VPPR.xls",
            "VPVH.xls",
            "VPTRPN.xls",
            "VPTRPR.xls",
            "VPTRPNL.xls",
            "VPTRPA.xls",
        ]
        
        # Asegúrate de que 'ruta_ventasperdidas' sea una propiedad de la clase
        self.ruta_ventasperdidas = None
        # Obtener la ruta base donde se almacenan los archivos
        self.ruta_base = self.variables.ruta_Trabajos_kwrb
        
    
            
            
    def crear_ventas_perdidas_iniciales(self):
        df_final_vacios =  pd.DataFrame()
        return df_final_vacios
            
    def venta_perdida_nuevo_laredo_matriz(self):
        documento = "VPNLM.xls"
        try:
            self.comprobar_documento(documento)
        except Exception as e:
            print(traceback.print_exc())
    def venta_perdida_reynosa(self):
        documento = "VPR.xls"
        self.comprobar_documento(documento)
    def venta_perdida_matamoros(self):
        documento = "VPM.xls"
        try:
            self.comprobar_documento(documento)
        except Exception as e:
            print(traceback.print_exc())
    def venta_perdida_piedras_negras(self):
        documento = "VPPN.xls"
        self.comprobar_documento(documento)
    def venta_perdida_nuevo_laredo_aeropuerto(self):
        documento = "VPNLA.xls"
        self.comprobar_documento(documento)
    def venta_perdida_poza_rica(self):
        documento = "VPPR.xls"
        self.comprobar_documento(documento)
    def venta_perdida_valle_hermoso(self):
        documento = "VPVH.xls"
        self.comprobar_documento(documento)
    def venta_perdida_trp_nava(self):
        documento = "VPTRPN.xls"
        self.comprobar_documento(documento)
    def venta_perdida_trp_reynosa(self):
        documento = "VPTRPR.xls"
        self.comprobar_documento(documento)
    def venta_perdida_trp_nuevo_laredo(self):
        documento = "VPTRPNL.xls"
        self.comprobar_documento(documento)
    def venta_perdida_trp_acuña(self):
        documento = "VPTRPA.xls"
        self.comprobar_documento(documento)
        
    def comprobar_documento(self, documento):
        self.comprobar_existencia_ventasperdidas()
        ruta_completa = os.path.join(self.ruta_base, documento)
        # Verificar si el archivo existe en la ruta
        if os.path.exists(ruta_completa):
            # Procesar el archivo actual
            df = self.proceso(documento)

            if df is not None:
                # Concatenar el DataFrame procesado al DataFrame final
                self.df_final = pd.concat([self.df_final, df], ignore_index=True)
                print(f'documento concatenado {documento}')

        # Si hemos procesado algún archivo, guardar el resultado final solo una vez al final
        if not self.df_final.empty:
            # Establecer la localización en español
            print(f'documento completo y guardado {documento}')
            self.variables.guardar_xls("ventasperdidas.xls", self.df_final, self.concesionario)
        
    def proceso(self, nombre_documento):
        self.nombre_doc = nombre_documento
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)

        # Leer el archivo Excel
        df = pd.read_excel(path, sheet_name=0)

        if df.empty:
            return None

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

        return df  # Devolver el DataFrame procesado

    def comprobar_existencia_ventasperdidas(self):
        # Buscar si ya existe un archivo con ventas perdidas
        for ventasperdidas in os.listdir(self.variables.ruta_exitosos_kwrb):
            if "ventasperdidas" in ventasperdidas:
                self.ruta_ventasperdidas = os.path.join(self.variables.ruta_exitosos_kwrb, ventasperdidas)

        # Comprobar si el archivo "ventasperdidas.xls" ya existe
        if self.ruta_ventasperdidas is not None:
            if os.path.exists(self.ruta_ventasperdidas):
                # Si el archivo existe, leer el archivo existente
                self.df_final = pd.read_excel(self.ruta_ventasperdidas)
                print(f"Archivo 'ventasperdidas.xls' encontrado y cargado.")
            else:
                print("El archivo 'ventasperdidas.xls' no existe en la ruta esperada.")
                self.df_final = self.crear_ventas_perdidas_iniciales()
        else:
            # Si no se ha encontrado el archivo en el directorio, crear uno nuevo
            print("No se encontró el archivo 'ventasperdidas.xls'. Creando archivo nuevo.")
            self.df_final = self.crear_ventas_perdidas_iniciales()