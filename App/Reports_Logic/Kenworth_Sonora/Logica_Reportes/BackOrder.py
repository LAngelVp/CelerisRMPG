"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
import numpy as np
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios 
class BackOrder(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
        self.nombre_doc = 'BOS.xlsx'

        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df2 = df.copy()
        df2.columns = df2.columns.str.replace(' ', '_')
        df2 = df2.rename(columns={ 'Número_BO': 'num'})
        df2.insert(
            loc  = 2,
            column = 'Número_BO',
            value = 'BO' + df2['num'].map(str),
            allow_duplicates = True
        )
        df2['Fecha_Hoy'] = self.variables.date_movement_config_document()

        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass

        df_no_nat = df2.query("Fecha_Alta_FC != ['NaT']").copy()
        df_no_nat["Antigüedad"] = (df_no_nat["Fecha_Hoy"] - df_no_nat["Fecha_Alta_FC"])

        df_nat = df2.query("Fecha_Alta_FC == ['NaT']").copy()
        df_nat["Antigüedad"] = (df_nat["Fecha_Hoy"] - df_nat["Fecha_Alta"])

        df_resta_fechas = pd.concat([df_no_nat, df_nat], join="inner")
        
        df_resta_fechas.drop(['Folio','Fecha_Hoy','Unidad_Relacionada', 'num'], axis=1, inplace=True)

        for column_name in df_resta_fechas.columns:
            if "fecha" in column_name.lower():
                df_resta_fechas = self.variables.global_date_format_dmy_mexican(df_resta_fechas, column_name)
            else:
                pass
        
        df_resta_fechas["Antigüedad"] = pd.to_timedelta(df_resta_fechas["Antigüedad"])
        df_resta_fechas["Antigüedad"] = df_resta_fechas["Antigüedad"].dt.days

        df_resta_fechas["Antigüedad"] = df_resta_fechas["Antigüedad"].apply(self.convertir_a_cero)
        
        columnas_bol=df_resta_fechas.select_dtypes(include=bool).columns.tolist()
        df_resta_fechas[columnas_bol] = df_resta_fechas[columnas_bol].astype(str)

        df_resta_fechas.columns = df_resta_fechas.columns.str.replace('_', ' ')

        self.variables.guardar_datos_dataframe(self.nombre_doc, df_resta_fechas, self.concesionario)

    def convertir_a_cero(self, valor):
        if valor < 0:
            return 0
        else:
            return valor

