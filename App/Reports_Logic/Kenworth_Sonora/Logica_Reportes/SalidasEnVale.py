"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class SalidasEnVale(Variables):
        def __init__(self):
            super().__init__()
            self.concesionario = Concesionarios().concesionarioSonora

            self.variables = Variables()
            self.nombre_doc = 'SVS.xlsx'
            path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
            df = pd.read_excel(path, sheet_name="Hoja2")
            df = df.replace(to_replace=';', value='-', regex=True)
            df_Sin_Requisiciones = df.query("Tipo != ['Requisiciones']").copy()
            df_format1 = df_Sin_Requisiciones[df_Sin_Requisiciones.columns[0:52]].copy()
            for column_name in df_format1.columns:
                if "fecha" in column_name.lower():
                    df_format1 = self.variables.global_date_format_america(df_format1, column_name)
                    df_format1 = self.variables.global_date_format_dmy_mexican(df_format1, column_name)
                else:
                    pass

            columnas_bol=df_format1.select_dtypes(include=bool).columns.tolist()
            df_format1[columnas_bol] = df_format1[columnas_bol].astype(str)
            
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_format1, self.concesionario)