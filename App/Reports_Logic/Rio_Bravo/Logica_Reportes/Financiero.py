"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ResultadosFinancieros(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        self.nombre_doc = 'RFR.xlsx'
            
        columnas = [
            "Sucursal",
            "Numarticulo",
            "idCliente",
            "NomDepto",
            "CondicionUnidad",
            "NombreCte",
            "idClienteAsignatario",
            "NombreCteAsignatario",
            "Vendedor",
            "NumCategoria",
            "Modelo",
            "cantidad",
            "Venta",
            "NC Bonif",
            "VentasNetas",
            "CostoTotal",
            "UtilidadBruta",
            "Compras",
            "VtasInternas",
            "NCreddeProv",
            "NCargodeProv",
            "ProvNCargoCargo",
            "ProvNCargoAbono",
            "ProvNCredCargo",
            "ProvNCredAbono",
            "NotaCargoCte"
        ]

        path = os.path.join(self.variables.ruta_Trabajos_kwrb,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        
        df_funcional = df[df["cantidad"] == 1].shape[0]
        
        if df_funcional <=0:
            return
        pivot = pd.pivot_table(df,
                        index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria'],
                        values=['cantidad', 'Venta', 'NC Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv', 'ProvNCargoCargo', 'ProvNCargoAbono', 'ProvNCredCargo', 'ProvNCredAbono', 'NotaCargoCte', 'CondicionUnidad', 'NomDepto', 'Vendedor'],
                        aggfunc='sum'
                        )
        pivot.reset_index(inplace=True)
        
        pivot = pivot.query("cantidad != 0")
        
        numarticulos_con_cantidades_negativas = pivot[pivot['cantidad'] < 0]['Numarticulo'].unique()

        pivot = pivot[~pivot['Numarticulo'].isin(numarticulos_con_cantidades_negativas)]
        

        pivot = pivot[columnas]

        if (len(pivot) == 0):
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot)
            
        else:
            pivot.insert(
                loc = 1,
                column = "ZonaVenta",
                value = pivot["Sucursal"],
                allow_duplicates=True
            )

            pivot.insert(
                loc = 16,
                column = "Margen(%)",
                value = pivot["UtilidadBruta"] / pivot["VentasNetas"],
                allow_duplicates=False
            )

            departamento = pivot["CondicionUnidad"].apply(lambda x: self.obtenerDepartamento(x))
            col_numero_articulo = "UN-" + pivot["Numarticulo"].map(str)
            col_modelo = "AM" + pivot["Modelo"].map(str)

            pivot["Numarticulo"] = col_numero_articulo
            pivot["Modelo"] = col_modelo

            pivot["Fecha"] = self.variables.date_movement_config_document().replace(day=1)
            pivot["Ciudad"] = "Pendiente"
            pivot["Estado"] = "Pendiente"



            pivot.insert(
                loc = 0,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )

            for column_name in pivot.columns:
                if "fecha" in column_name.lower():
                    pivot = self.variables.global_date_format_america(pivot, column_name)
                    pivot = self.variables.global_date_format_dmy_mexican(pivot, column_name)
                else:
                    pass

            columnas_bol=pivot.select_dtypes(include=bool).columns.tolist()
            pivot[columnas_bol] = pivot[columnas_bol].astype(str)
            
            pivot.drop(['NomDepto', 'CondicionUnidad'], axis=1, inplace=True)

            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)
        
    def obtenerDepartamento(self, valor):
            if (valor.lower() == "usado"):
                return "Unidades Seminuevas"
            else:
                return "Unidades Nuevas"
