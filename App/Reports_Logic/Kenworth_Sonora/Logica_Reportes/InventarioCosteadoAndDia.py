"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class InventarioCosteado(Variables):
    def __init__(self):
        super().__init__()
        self.nombre_doc = 'ICS.xlsx'
        self.nombre_doc2 = 'ICDS.xlsx'
        
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()

        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=";", value="-", regex=True)
        df2 = df[df.columns[0:33]].copy()
        df2.insert(loc=28,column="Fecha_Hoy",value=self.variables.date_movement_config_document(), allow_duplicates=False)
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass
        Antiguedad = (df2["Fecha_Hoy"] - df2["Fecha Entrada"]).apply(lambda x : x.days)
        df2.insert(loc=28,column="Antigüedad",value=Antiguedad,allow_duplicates=False)
        df2 = df2.sort_values(by=["Antigüedad"],ascending=True)
        df2["ClasDias"] = ""
        for index, valor in df2["Antigüedad"].items():
            if (valor < 0):
                try:
                    df2.loc[index,"Antigüedad"] = 0
                except:
                    pass
            else:
                pass
        
        df2["ClasDias"] = df2["Antigüedad"].apply(lambda x:self.ClasDias(x))
        for column_name in df2.columns:
            if "fecha entrada" in column_name.lower():
                df2 = self.variables.global_date_format_mdy_america(df2, column_name)
            elif "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
        df2.drop(["Fecha_Hoy"], axis=1, inplace=True)
        df_inventarioCosteado = df2.copy()
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_inventarioCosteado, self.concesionario)

        df_inventarioCosteadoxDia = df2.copy()
        df_inventarioCosteadoxDia= self.variables.global_date_format_america(df_inventarioCosteadoxDia, "Fecha Entrada")
        df_inventarioCosteadoxDia= self.variables.global_date_format_dmy_mexican(df_inventarioCosteadoxDia, "Fecha Entrada")
        df_inventarioCosteadoxDia.drop(["Antigüedad","ClasDias"],axis=1,inplace=True)
        df_inventarioCosteadoxDia["Fecha_Dias"] = self.variables.date_movement_config_document()
        df_inventarioCosteadoxDia["ClasSF"] = ""

        df_inventarioCosteadoxDia["ClasSF"] = df_inventarioCosteadoxDia.apply(lambda fila:self.ClasSF_TipoDocumento(fila["TipoDocumento"], fila["ClasSF"]),axis=1)

        df_inventarioCosteadoxDia["ClasSF"] = df_inventarioCosteadoxDia.apply(lambda fila:self.ClasSF_Almacen(fila["Almacén"],fila["TipoDocumento"], fila["ClasSF"]),axis=1)

        df_inventarioCosteadoxDia["Mes"] = self.variables.nombre_mes_actual_abreviado()

        df_inventarioCosteadoxDia= self.variables.global_date_format_america(df_inventarioCosteadoxDia, "Fecha_Dias")

        df_inventarioCosteadoxDia= self.variables.global_date_format_dmy_mexican(df_inventarioCosteadoxDia, "Fecha_Dias")

        self.variables.guardar_datos_dataframe(self.nombre_doc2, df_inventarioCosteadoxDia, self.concesionario)

    def ClasDias(self, valor):
        if (valor >= 0 and valor <= 90):
            return "1 a 90"
        elif (valor >= 91 and valor <= 180):
            return "91 a 180"
        elif (valor >= 181 and valor <= 270):
            return "181 a 270"
        elif (valor >= 271 and valor <= 360):
            return "271 a 360"
        elif (valor >= 361):
            return "Mas de 360"
        else:
            pass

    def ClasSF_TipoDocumento(self, valor_TipoDocumento,valor_almacen):
        if (valor_TipoDocumento.lower() == "inventario"):
            return "Almacen"
        elif (valor_TipoDocumento.lower() == "requisiciones"):
            return "Requisiciones"
        elif (valor_TipoDocumento.lower() == "salidas en vale"):
            return "Salidas en Vale"
        elif ((valor_TipoDocumento.lower() == "traspaso de entrada") | (valor_TipoDocumento == "traspaso de salida")):
            return "Traspaso"
        elif (valor_TipoDocumento.lower() == "venta"):
            return "Venta"
        else:
            return valor_almacen
        
    def ClasSF_Almacen(self, valor_almacen,tipo_documento, valor_clasSF):
        if (("consigna" in valor_almacen.lower()) and "inventario" in tipo_documento.lower()):
            return "Consignas"
        elif ("rescates" in valor_almacen.lower() or "rescate" in valor_almacen.lower() and "inventario" in tipo_documento.lower()):
            return "Rescates"
        else:
            return valor_clasSF
        