#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ResultadosFinancierosKREI(Variables):
    def __init__(self) -> None:
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

        self.columnas = [
            "Numarticulo",
            "idCliente",
            "NomDepto",
            "CondicionUnidad",
            "NombreCte",
            "idClienteAsignatario",
            "NombreCteAsignatario",
            "NumCategoria",
            "Modelo",
            "Sucursal",
            "cantidad",
            "Venta",
            "NC_Bonif",
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
            "NotaCargoCte",
            "Vendedor"
        ]

    def ReporteFinancieroKWESTE_KREI(self):
        self.nombre_doc = 'RFEKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(path, sheet_name="Hoja2")
        df.columns = df.columns.str.replace(" ", "_")
        
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
        
        pivot = pivot[self.columnas]

        if (len(pivot) == 0):
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)
            
        else:
            pivot.insert(
                    loc = 0,
                    column = "Concesionario",
                    value = "KW ESTE",
                    allow_duplicates=True
                )
            
            departamento = pivot["CondicionUnidad"].apply(lambda x: self.obtenerDepartamento(x))

            pivot.insert(
                loc = 1,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )


            col_numero_articulo = "CH-" + pivot["Numarticulo"].map(str)
            col_modelo = "AM" + pivot["Modelo"].map(str)

            pivot["Numarticulo"] = col_numero_articulo
            pivot["Modelo"] = col_modelo

            Margen = pivot["UtilidadBruta"] / pivot["VentasNetas"]

            pivot.insert(
                loc = 18,
                column = "Margen(%)",
                value = Margen,
                allow_duplicates = True
            )

            Fecha = self.variables.date_movement_config_document()

            pivot.insert(
                loc = 28,
                column = "Fecha",
                value = Fecha,
                allow_duplicates = True
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

            pivot.columns = pivot.columns.str.replace("_", " ")

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)


    def ReporteFinancieroKWSUR_KREI(self):
        self.nombre_doc = 'RFSKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # LEEMOS EL DOCUMENTO
        df = pd.read_excel(path, sheet_name="Hoja2")
        df.columns = df.columns.str.replace(" ", "_")
        
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
        
        pivot = pivot[self.columnas]

        if (len(pivot) == 0):
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)
            
        else:
            pivot.insert(
                    loc = 0,
                    column = "Concesionario",
                    value = "KW SUR",
                    allow_duplicates=True
                )
            departamento = pivot["CondicionUnidad"].apply(lambda x: self.obtenerDepartamento(x))

            pivot.insert(
                loc = 1,
                column = "Departamento",
                value = departamento,
                allow_duplicates = False
            )


            col_numero_articulo = "CH-" + pivot["Numarticulo"].map(str)
            col_modelo = "AM" + pivot["Modelo"].map(str)

            pivot["Numarticulo"] = col_numero_articulo
            pivot["Modelo"] = col_modelo

            Margen = pivot["UtilidadBruta"] / pivot["VentasNetas"]

            pivot.insert(
                loc = 18,
                column = "Margen(%)",
                value = Margen,
                allow_duplicates = True
            )

            Fecha = self.variables.date_movement_config_document()

            pivot.insert(
                loc = 28,
                column = "Fecha",
                value = Fecha,
                allow_duplicates = True
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
            
            pivot = pivot[columnas]

            pivot.columns = pivot.columns.str.replace("_", " ")

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)


    def obtenerDepartamento(self,valor):
            # currentYear = self.variables.fecha_hoy.year
            if (valor.lower() == "usado"):
                return "SEMINUEVAS"
            else:
                return "NUEVAS"
            