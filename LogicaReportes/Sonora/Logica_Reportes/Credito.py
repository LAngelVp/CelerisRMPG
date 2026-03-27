"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Credito(Variables):
    def __init__(self):
        super().__init__()
        self.nombre_doc = 'CS.xlsx'
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()

        path =  os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name="Hoja2")
        df2 = df[df.columns[0:52]].copy()
        df2 = df2.replace(to_replace = ";", value = "_", regex = True)
        df2.columns = df2.columns.str.replace(" ", "_")
        df2.insert(loc=2,column="Clasificacion",value="CLIENTES GENERALES", allow_duplicates = False)
        array_excepto_clientes = ["KENWORTH","PACCAR PARTS MEXICO", "PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA", "DISTRIBUIDORA MEGAMAK", "SEGUROS", "SEGURO", "GRUPO NACIONAL PROVINCIAL"]
        df2.loc[df2["Cliente"].str.contains("KENWORTH") & ~df2["Cliente"].str.contains("KENWORTH MEXICANA"), "Clasificacion"] = "CONCESIONARIOS"
        df2.loc[df2["Cliente"] == "KENWORTH MEXICANA", "Clasificacion"] = "KENMEX"
        df2.loc[df2["Cliente"] == "PACCAR PARTS MEXICO", "Clasificacion"] = "PACCAR PARTS"
        df2.loc[df2["Cliente"] == "DISTRIBUIDORA MEGAMAK", "Clasificacion"] = "MEGAMAK"
        df2.loc[(df2["Cliente"] == "PACCAR FINANCIAL MEXICO") | (df2["Cliente"] == "PACLEASE MEXICANA"), "Clasificacion"] = "PLM"
        df2.loc[(df2["Cliente"].str.contains('SEGUROS')) | (df2["Cliente"].str.contains('SEGURO')) | (df2["Cliente"] == 'GRUPO NACIONAL PROVINCIAL'), "Clasificacion" ]= "SEGUROS"
        df2.loc[~df2["Cliente"].str.contains("|".join(array_excepto_clientes)), "Clasificacion"] = "CLIENTES GENERALES"

        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
            else:
                pass

        valor_loc = 1
        for columna in df2:
            if ("fecha_vencimiento" == columna.lower()):
                df2.insert(loc=valor_loc, column="Semana", value = "S-" + (df2["Fecha_Vencimiento"].dt.isocalendar().week).map(str), allow_duplicates=False)
            valor_loc +=1

        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
            else:
                pass

        df2.columns = df2.columns.str.replace("_", " ")

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)


        self.nombre_doc = 'CSG.xlsx'
        CreditoGlobal = df2.copy()
        CreditoGlobal.drop(["Clasificacion","Semana"], axis=1, inplace=True) 
        CreditoGlobal["Mes"] = self.variables.nombre_mes_actual_abreviado()

        self.variables.guardar_datos_dataframe(self.nombre_doc, CreditoGlobal, self.concesionario)
