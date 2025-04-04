#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ResultadosFinancieros(Variables):
    def __init__(self):
        # FUNCION PARA OBTENER EL DEPARTAMENTO
            
        # CREAMOS UN ARRAY CON EL NOMBRE DE LAS COLUMNAS QUE VAMOS A OCUPAR DEL DATAFRAME ORIGINAL
        # ESTE ARRAY SE VA A OCUPAR MAS ADELANTE PARA CREAR EL DATAFRAME FINAL.
        
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

        # OBTENEMOS LA RUTA DEL ARCHIVO Y PARSEAMOS SU CONTENIDO Y SUS CABECERAS.
        path = os.path.join(self.variables.ruta_Trabajos_kwrb,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        
        df_funcional = df[df["cantidad"] == 1].shape[0]
        
        if df_funcional <=0:
            return
        # creamos la tabla pivote, con el fin de obtener las unidades facturadas
        pivot = pd.pivot_table(df,
                        index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria'],
                        values=['cantidad', 'Venta', 'NC_Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv', 'ProvNCargoCargo', 'ProvNCargoAbono', 'ProvNCredCargo', 'ProvNCredAbono', 'NotaCargoCte', 'CondicionUnidad', 'NomDepto', 'Vendedor'],
                        aggfunc='sum'
                        )
        
        # eliminamos el formato de la tabla pivote, con la finalidas de aparecer los numeros que la tabla pivote maneja como vacios
        pivot.reset_index(inplace=True)
        
        pivot = pivot.query("cantidad != 0")
        
        # Identificar los 'Numarticulo' que tienen cantidades negativas
        numarticulos_con_cantidades_negativas = pivot[pivot['cantidad'] < 0]['Numarticulo'].unique()

        # Eliminar todas las filas que contienen esos 'Numarticulo' con cantidad negativa
        pivot = pivot[~pivot['Numarticulo'].isin(numarticulos_con_cantidades_negativas)]
        

        pivot = pivot[columnas]

        if (len(pivot) == 0):
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
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

    # TERMINAMOS DE INSERTAR COLUMNAS ------------------

            # FORMATEAMOS LAS COLUMNAS DE FECHA

            for column_name in pivot.columns:
                if "fecha" in column_name.lower():
                    pivot = self.variables.global_date_format_america(pivot, column_name)
                    pivot = self.variables.global_date_format_dmy_mexican(pivot, column_name)
                else:
                    pass

            # BUSCAMOS COLUMNAS QUE SEAN DE TIPO BOOLEANO, SI LAS ENCUENTRA, QUE LAS CONVIERTA EN CADENA.

            columnas_bol=pivot.select_dtypes(include=bool).columns.tolist()
            pivot[columnas_bol] = pivot[columnas_bol].astype(str)
            
            pivot.drop(['NomDepto', 'CondicionUnidad'], axis=1, inplace=True)

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)
        
    def obtenerDepartamento(self, valor):
            # currentYear = datetime.now().year
            if (valor.lower() == "usado"):
                return "Unidades Seminuevas"
            else:
                return "Unidades Nuevas"
