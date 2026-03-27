"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class InventarioKWESTEKREI(Variables):

    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

    def InventarioKWESTE_KREI(self):
        self.nombre_doc = 'ICEKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei,self.nombre_doc)
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=";", value="-", regex=True)
        df2 = df[df.columns[0:33]].copy()

        df2.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)

        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_america(df2, column_name)
                else:
                    pass

        antiguedad = self.variables.date_movement_config_document() - df2["Fecha Entrada"]

        df2["Antigüedad"] =  antiguedad.dt.days


        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
                else:
                    pass

        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        df2["ClassAlmacen"] = "Inventario"

        df2.loc[df2["Almacén"].str.lower().str.contains("infan"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.lower().str.contains("mx"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("t380"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("t680"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("daf"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.lower().str.contains("kw45"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.lower().str.contains("servicio express"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("ultrashift"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[(df2["Almacén"].str.lower().str.contains("rescates")) | 
                                    (df2["Almacén"].str.lower().str.contains("rescate")), "ClassAlmacen"] = "Inventario de Seguridad"


        df2.loc[(df2["Almacén"].str.lower().str.contains("con m")) | 
                                     ( df2["Almacén"].str.lower().str.contains("consig")), "ClassAlmacen"] = "Consigna"

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
    
    def InventarioKWSUR_KREI(self):
        self.nombre_doc = 'ICSKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=";", value="-", regex=True)
        df2 = df[df.columns[0:33]].copy()

        df2.insert(0,"Concesionario","KW SUR", allow_duplicates=False)

        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_america(df2, column_name)
                else:
                    pass

        antiguedad = self.variables.date_movement_config_document() - df2["Fecha Entrada"]

        df2["Antigüedad"] =  antiguedad.dt.days


        for column_name in df2.columns:
                if "fecha" in column_name.lower():
                    df2 = self.variables.global_date_format_dmy_mexican(df2, column_name)
                else:
                    pass
            
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        df2["ClassAlmacen"] = "Inventario"

        df2.loc[df2["Almacén"].str.lower().str.contains("infan"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.lower().str.contains("mx"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("t380"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("t680"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("daf"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.lower().str.contains("kw45"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[df2["Almacén"].str.lower().str.contains("servicio express"), "ClassAlmacen"] = "Inventario de Seguridad"
        
        df2.loc[df2["Almacén"].str.lower().str.contains("ultrashift"), "ClassAlmacen"] = "Inventario de Seguridad"

        df2.loc[(df2["Almacén"].str.lower().str.contains("rescates")) | 
                                    (df2["Almacén"].str.lower().str.contains("rescate")), "ClassAlmacen"] = "Inventario de Seguridad"


        df2.loc[(df2["Almacén"].str.lower().str.contains("consigna")) | 
                                    ( df2["Almacén"].str.contains("consignas")), "ClassAlmacen"] = "Consigna"

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
