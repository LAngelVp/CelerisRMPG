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
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
            
        columnas = [
            'Departamento',
            "Numarticulo",
            "Sucursal",
            "Modelo",
            "idCliente",
            "NombreCte",
            "idClienteAsignatario",
            "NombreCteAsignatario",
            "Vendedor",
            "NumCategoria",
            "cantidad",
            "Venta",
            "NC_Bonif",
            "VentasNetas",
            "CostoTotal",
            "UtilidadBruta",
            'Margen(%)',
            "Compras",
            "VtasInternas",
            "NCreddeProv",
            "NCargodeProv",
            "ProvNCargoCargo",
            "ProvNCargoAbono",
            "ProvNCredCargo",
            "ProvNCredAbono",
            "NotaCargoCte",
            "InteresesPP",
            'Fecha',
            'Mes',
            'Ciudad',
            'Estado'
        ]

        # OBTENEMOS LA RUTA DEL ARCHIVO Y PARSEAMOS SU CONTENIDO Y SUS CABECERAS.
        self.nombre_doc = 'RFS.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(" ", "_")
        
        df_funcional = df[df["cantidad"] == 1].shape[0]
        
        if df_funcional <=0:
            return
        # creamos la tabla pivote, con el fin de obtener las unidades facturadas
        pivot = pd.pivot_table(df,
                        index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria'],
                        values=['cantidad', 'Venta', 'NC_Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv', 'ProvNCargoCargo', 'ProvNCargoAbono', 'ProvNCredCargo', 'ProvNCredAbono', 'NotaCargoCte', 'CondicionUnidad', 'NomDepto', 'Vendedor', 'InteresesPP'],
                        aggfunc='sum'
                        )
        
        # eliminamos el formato de la tabla pivote, con la finalidas de aparecer los numeros que la tabla pivote maneja como vacios
        pivot.reset_index(inplace=True)
        
        pivot = pivot.query("cantidad != 0")
        
        # Identificar los 'Numarticulo' que tienen cantidades negativas
        numarticulos_con_cantidades_negativas = pivot[pivot['cantidad'] < 0]['Numarticulo'].unique()

        # Eliminar todas las filas que contienen esos 'Numarticulo' con cantidad negativa
        pivot = pivot[~pivot['Numarticulo'].isin(numarticulos_con_cantidades_negativas)]

        if (len(pivot) == 0):
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)

        else:
            pivot.insert(
                loc = 15,
                column = "Margen(%)",
                value = pivot["UtilidadBruta"] / pivot["VentasNetas"],
                allow_duplicates = True
            )

            
            departamento = pivot["CondicionUnidad"].apply(lambda x: self.obtenerDepartamento(x))

            pivot.insert(
                loc = 0,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )

            col_numero_articulo ="CH-" + pivot["Numarticulo"].map(str)
            col_modelo ="AM-" + pivot["Modelo"].map(str)

            pivot["Numarticulo"] = col_numero_articulo
            pivot["Modelo"] = col_modelo


            pivot["Fecha"] = self.variables.date_movement_config_document().replace(day=1)
            pivot["Mes"] = self.variables.nombre_mes_actual_abreviado()
            pivot["Ciudad"] = "Pendiente"
            pivot["Estado"] = "Pendiente"

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
            
            pivot.drop(['CondicionUnidad'], axis=1, inplace=True)
            
            pivot = pivot[columnas]

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)
            
    def obtenerDepartamento(self, valor):
        # currentYear = datetime.now().year
        if (valor.lower() == "usado"):
            return "VENTA DE UNIDADES USADAS"
        else:
            return "VENTA DE UNIDADES NUEVAS"