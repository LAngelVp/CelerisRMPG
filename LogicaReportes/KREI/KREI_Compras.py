"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ComprasKREI(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

    def ComprasSur(self):
        self.nombre_doc = 'CDSKREI.xlsx'
        path =  os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace = ";", value = "_", regex = True)
        COLUMNS_DATE = [col for col in df.columns 
                        if "fecha" in col.lower()
                        ]
        for column_name in COLUMNS_DATE:
            df = self.variables.global_date_format_america(df, column_name)
            df = self.variables.global_date_format_dmy_mexican(df, column_name)

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
