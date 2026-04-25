"""
DESARROLLADOR
LUIS A. PEREZ
"""
from decimal import Decimal
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import pandas as pd
from datetime import *
import numpy as np
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class OrdenesDeServicio(Variables):
    def __init__(self):
        super().__init__()
        self.nombre_doc = 'OSS.xlsx'
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()

        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        
        df = pd.read_excel(path, sheet_name="Hoja2")
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(' ', '_')
        df2 = df.copy()

        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]

        df2.insert(loc=5,column="Clasificacion_Cliente",value="CLIENTES GENERALES", allow_duplicates = False)

        df2.loc[df2["Cliente"].str.contains("KENWORTH") & ~df2["Cliente"].str.contains("KENWORTH MEXICANA") & ~df2["Cliente"].str.contains("KENWORTH DISTRIBUIDORA DE SONORA"), "Clasificacion_Cliente"] = "CONCESIONARIOS"
        df2.loc[df2["Cliente"].str.contains("|".join(array_Garantia)),"Clasificacion_Cliente"] = "GARANTIA"
        df2.loc[df2["Cliente"].str.contains("|".join(array_PLM)),"Clasificacion_Cliente"] = "PLM"
        df2.loc[df2["Cliente"] == "KENWORTH DISTRIBUIDORA DE SONORA", "Clasificacion_Cliente"] = "CI"
        df2.loc[(df2["Cliente"].str.contains("SEGUROS")) | (df2["Cliente"].str.contains("SEGURO")) | (df2["Cliente"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion_Cliente"] = "SEGUROS"

        QuitamosGarantia = df2.query("~(Clasificacion_Cliente == ['GARANTIA'])").copy()
        TomamosGarantia = df2.query("Clasificacion_Cliente == ['GARANTIA']").copy()

        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Externo"),"Clasificacion_Cliente"] = "RESCATES EXTERNOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Rescate Avalado"), "Clasificacion_Cliente"] = "RESCATES AVALADOS"
        QuitamosGarantia.loc[QuitamosGarantia["Tipo_Servicio"].str.contains("Taller Móvil"), "Clasificacion_Cliente"] = "TALLER MOVIL"

        claficicacion_tipo_servicio = pd.concat([QuitamosGarantia, TomamosGarantia], join="inner")

        NumOrden = "OS" + claficicacion_tipo_servicio["Número_Orden"].map(str)
        Unidad = "UN-" + claficicacion_tipo_servicio["Unidad"].map(str)
        
        claficicacion_tipo_servicio.insert(0,"Num_Orden",NumOrden,allow_duplicates=True)
        claficicacion_tipo_servicio["Unidad"] = Unidad

        claficicacion_tipo_servicio.drop(["Número_Orden","Folio_Cotizaciones"], axis = 1, inplace=True)
        ultima_columna = claficicacion_tipo_servicio.columns.get_loc("Estado_Orden_Global")
        claficicacion_tipo_servicio = claficicacion_tipo_servicio.iloc[:,:ultima_columna + 1]
        Clasificacion_Venta = claficicacion_tipo_servicio["Clasificacion_Cliente"]
        claficicacion_tipo_servicio.insert(6,"Clasificacion_Venta",Clasificacion_Venta,allow_duplicates=False)
        

        for column_name in claficicacion_tipo_servicio.columns:
            if "fecha" in column_name.lower():
                claficicacion_tipo_servicio = self.variables.global_date_format_america(claficicacion_tipo_servicio, column_name)
            else:
                pass

        columna = claficicacion_tipo_servicio.pop("Subtotal_Ref_Sin_Facturar")
        claficicacion_tipo_servicio.insert(21, "Subtotal_Ref_Sin_Facturar", columna)
        claficicacion_tipo_servicio.insert(loc=25, column = 'Total OS Pde Fact', value = claficicacion_tipo_servicio[['MO', 'CM', 'TOT', 'Subtotal_Ref_Sin_Facturar']].fillna(0).sum(axis=1), allow_duplicates = False)

        claficicacion_tipo_servicio['Total OS Pde Fact'] = claficicacion_tipo_servicio['Total OS Pde Fact'].apply(lambda x: '{:.2f}'.format(x))
        claficicacion_tipo_servicio['Total OS Pde Fact'] = claficicacion_tipo_servicio['Total OS Pde Fact'].astype(float).fillna(0)

        claficicacion_tipo_servicio.columns = claficicacion_tipo_servicio.columns.str.replace('_', ' ')
        claficicacion_tipo_servicio["Cantidad_Trabajos"] = 1

        for column_name in claficicacion_tipo_servicio.columns:
            if "fecha" in column_name.lower():
                claficicacion_tipo_servicio = self.variables.global_date_format_dmy_mexican(claficicacion_tipo_servicio, column_name)
            else:
                pass
        
        columnas_bol=claficicacion_tipo_servicio.select_dtypes(include=bool).columns.tolist()
        claficicacion_tipo_servicio[columnas_bol] = claficicacion_tipo_servicio[columnas_bol].astype(str)

        claficicacion_tipo_servicio['Id_Personalizado'] = claficicacion_tipo_servicio['Num Orden'] + ' - ' + claficicacion_tipo_servicio['Sucursal']

        self.variables.guardar_datos_dataframe(self.nombre_doc, claficicacion_tipo_servicio, self.concesionario)