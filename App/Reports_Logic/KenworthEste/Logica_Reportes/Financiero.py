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
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.nombre_doc = 'RFE.xlsx'
        # CREAMOS UN ARRAY CON EL NOMBRE DE LAS COLUMNAS QUE VAMOS A OCUPAR DEL DATAFRAME ORIGINAL
        # ESTE ARRAY SE VA A OCUPAR MAS ADELANTE PARA CREAR EL DATAFRAME FINAL.
            
        columnas = [
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

        # OBTENEMOS LA RUTA DEL ARCHIVO Y PARSEAMOS SU CONTENIDO Y SUS CABECERAS.
        
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
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

        pivot.reset_index(inplace=True)
        
        pivot = pivot.query("cantidad != 0")
        
        numarticulos_con_cantidades_negativas = pivot[pivot['cantidad'] < 0]['Numarticulo'].unique()
        
        pivot = pivot[~pivot['Numarticulo'].isin(numarticulos_con_cantidades_negativas)]
        
        pivot = pivot[columnas]
        
        if (len(pivot) == 0):
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)

        else:
            pivot.insert(
                loc = 15,
                column = "Margen(%)",
                value = pivot["UtilidadBruta"] / pivot["VentasNetas"],
                allow_duplicates=False
            )

            departamento = pivot["CondicionUnidad"].apply(lambda x: self.obtenerDepartamento(x))
            col_numero_articulo = "CH-" + pivot["Numarticulo"].astype(str).str.rstrip(".0")
            col_modelo = "AM" + pivot["Modelo"].map(str)

            pivot["Numarticulo"] = col_numero_articulo
            pivot["Modelo"] = col_modelo

            pivot["Fecha"] = self.variables.date_movement_config_document()
            


            pivot.insert(
                loc = 0,
                column = "Categoria",
                value = "Facturacion",
                allow_duplicates = False
            )

            pivot.insert(
                loc = 1,
                column = "Area",
                value = departamento,
                allow_duplicates = False
            )

            pivot.insert(
                loc = 2,
                column = "Departamento",
                value = pivot["Area"].str.upper(),
                allow_duplicates = False
            )
            
            pivot.insert(
                loc = 4,
                column = "Fecha Vta",
                value = "",
                allow_duplicates = False
            )
            
            pivot.insert(
                loc = 5,
                column = "Zona Vta",
                value = "",
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
            
            pivot = self.clientes_financiero_merge(pivot)
            pivot["Status"] = ""
            pivot["Mes"] = self.variables.nombre_mes()
            pivot["colum_vacia"] = ""
            pivot["colum_vacia2"] = ""
            pivot = self.coordenadas_financiero_merge(pivot)
            
            
            pivot["Sucursal"] = pivot["Sucursal"].replace("Matriz Cordoba", "Venta Parada")
            pivot["Sucursal"] = pivot["Sucursal"].replace("Tuxtla1", "Chiapas")
            
            pivot.loc[pivot["Sucursal"] == "Venta Parada", "Zona Vta"] = "Cordoba/Orizaba"
            pivot.loc[pivot["Sucursal"] == "Oaxaca", "Zona Vta"] = "Oaxaca"
            pivot.loc[pivot["Sucursal"] == "Chiapas", "Zona Vta"] = "Tuxtla Guitierrez"
            pivot.loc[pivot["Sucursal"] == "Veracruz", "Zona Vta"] = "Veracruz/Xalapa"
            pivot.loc[pivot["Sucursal"] == "Villahermosa", "Zona Vta"] = "Villa/Coatza/Campeche"
            
            

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, pivot, self.concesionario)
        
    def obtenerDepartamento(self, valor):
            # currentYear = datetime.now().year
            if (valor.lower() == "usado"):
                return "Venta de Unidades Usadas"
            else:
                return "Venta de Unidades Nuevas"
    
    def coordenadas_financiero_merge(self, data):
        coordenadas = pd.read_json(os.path.join(self.variables.help_directory, self.variables.coordenadas_financiero))
        coordenadas = coordenadas.drop_duplicates(subset="Sucursal", keep="last")
        nuevo_data =  data.merge(coordenadas[["Sucursal", "SucursalMap", "Latitud", "Longitud"]], on="Sucursal", how="left")
        return nuevo_data
    
    def clientes_financiero_merge(self, data):
        clientes = pd.read_json(os.path.join(self.variables.help_directory, self.variables.clientes_financiero))
        clientes = clientes.drop_duplicates(subset="NombreCteAsignatario", keep="last")
        nuevo_data =  data.merge(clientes[["NombreCteAsignatario", "Ciudad", "Estado"]], on="NombreCteAsignatario", how="left")
        return nuevo_data

    
