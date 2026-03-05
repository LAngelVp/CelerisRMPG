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
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        self.nombre_doc = "BOR.xlsx"
        path = os.path.join(self.variables.ruta_Trabajos_kwrb,self.nombre_doc)

        try:
            df = pd.read_excel(path, sheet_name='Hoja2')
        except FileNotFoundError:
            pass

        df = df.replace(to_replace=';', value='-', regex=True)
        df2 = df.copy()
        df2 = df2.rename(columns={ 'Número BO': 'num'})
        df2.insert(
            loc  = 2,
            column = 'Número BO',
            value = 'BO' + df2['num'].map(str),
            allow_duplicates = True
        )
        df2['Fecha_Hoy'] = self.variables.date_movement_config_document()

        EXCLUDE_COLUMN_DATE = ["días bo sin facturar fecha alta"]
        COLUMNS_DATE = [col for col in df2.columns 
                        if "fecha" in col.lower() and col.lower().strip() not in EXCLUDE_COLUMN_DATE
                        ]
        for column_name in COLUMNS_DATE:
            df2 = self.variables.global_date_format_america(df2, column_name)
        
        df_no_nat = df2[df2['Fecha Alta FC'].notna()].copy()
        df_no_nat["Antigüedad"] = df_no_nat["Fecha_Hoy"] - df_no_nat["Fecha Alta FC"]

        df_nat = df2[df2['Fecha Alta FC'].isna()].copy()
        df_nat["Antigüedad"] = df_nat["Fecha_Hoy"] - df_nat["Fecha Alta"]

        df_resta_fechas = pd.concat([df_no_nat, df_nat], join="inner")
        
        df_resta_fechas.drop(['Folio','Fecha_Hoy','Unidad Relacionada', 'num'], axis=1, inplace=True)

        for column_name in COLUMNS_DATE:
            df_resta_fechas = self.variables.global_date_format_dmy_mexican(df_resta_fechas, column_name)

        df_resta_fechas["Antigüedad"] = pd.to_timedelta(df_resta_fechas["Antigüedad"])
        df_resta_fechas["Antigüedad"] = df_resta_fechas["Antigüedad"].dt.days

        df_resta_fechas["Antigüedad"] = df_resta_fechas["Antigüedad"].apply(self.convertir_a_cero)

        columnas_bol=df_resta_fechas.select_dtypes(include=bool).columns.tolist()
        df_resta_fechas[columnas_bol] = df_resta_fechas[columnas_bol].astype(str)

        for column in df_resta_fechas['Antigüedad']:
            if (column < (0)):
                df_resta_fechas['Antigüedad'] = df_resta_fechas['Antigüedad'].replace(column,0)
            else:
                pass
        
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_resta_fechas, self.concesionario)

    def convertir_a_cero(self, valor):
        if valor < 0:
            return 0
        else:
            return valor