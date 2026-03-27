"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class ServioDetallado(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        self.nombre_doc = "SDR.xlsx"
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        lista_garantia = ["KENWORTH MEXICANA", "ALESSO", "PACCAR PARTS MEXICO"]
        lista_plm = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]
        tipo_servicio_taller_movil = ["TM", "Taller Movil"]
        array_columns = ['ObjRefacc','ObjUBTRef','ObjMO', 'ObjUTBMO','Clasificacion Cliente']

        x = 3
        for i in array_columns:
            if (x <= 6):
                df.insert(
                    loc = x,
                    column = i,
                    value = 0,
                    allow_duplicates = False
                )
            else:
                df.insert(
                    loc = x,
                    column = i,
                    value = 'CLIENTES GENERALES',
                    allow_duplicates = False
                )
            x = x+1
        array_columns2 = ['Departamento Venta', 'Departamento']
        y = 22
        for i in array_columns2:
            df.insert(
                loc = y,
                column = i,
                value = '',
                allow_duplicates = False
            )
            y = y+1
        numero_orden = 'OS' + df["Número Orden"].astype(str).str.split(".").str[0].replace("nan","").fillna("")
        df["Número Orden"] = numero_orden
        df["Unidad"] = df["Unidad"].fillna("")
        unidad = "UN-" + df["Unidad"]
        df["Unidad"] = unidad
        df["Cliente"] = df["Cliente"].fillna("")
        df.loc[df["Cliente"].str.contains("KENWORTH"), "Clasificacion Cliente"] = "CONCESIONARIOS"
        df.loc[df["Cliente"] == "", "Clasificacion Cliente"] = "CI"
        df.loc[df["Cliente"].str.contains("|".join(lista_plm)), "Clasificacion Cliente"] = "PLM"
        df.loc[df["Cliente"].str.contains("|".join(lista_garantia)), "Clasificacion Cliente"] = "GARANTIA"
        df["Departamento Venta"] = "Servicio"
        df["Departamento"] = ""
        df["Departamento"] = df.apply(lambda fila: self.clasificacion_servicio(fila["Sucursal"]), axis=1)
        pattern = "|".join(tipo_servicio_taller_movil)
        df[["Departamento Venta", "Departamento"]] = df.apply(
            lambda fila: (
                self.clasificacion_taller_movil(fila["Sucursal"]) 
                if pd.Series(str(fila["Tipo Servicio"])).str.contains(pattern, case=False, regex=True).any()
                else [fila["Departamento Venta"], fila["Departamento"]]
            ),
            axis=1,
            result_type="expand"
        )
        df["Area"] = df.apply(
            lambda fila : self.clasificacion_area(fila["Departamento Venta"], fila["DepartamentoDetalle"]),
            axis=1
            )
        df.insert(10,"Fecha Movimiento",self.variables.date_movement_config_document(),allow_duplicates=False)
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)
        df.drop(
            [
                "Hora Docto.",
                "Fecha Cancelación",
                "Id. Paquete",
                "Paquete",
                "Descripción Paquete",
                "Cantidad Paquete",
                "Subtotal Paquete",
                "Saldo",
            ],
            axis=1,
            inplace=True
        )
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)
                df = self.variables.global_date_format_dmy_mexican(df, column_name)
                
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
        
    def clasificacion_servicio(self, sucursal = None):
        if sucursal == "MATAMOROS":
            return "Servicio Matamoros"
        elif sucursal == "NUEVO LAREDO (AEROPUERTO)":
            return "Servicio NL Matriz"
        elif sucursal == "NUEVO LAREDO (MATRIZ)":
            return "Servicio NL Matriz"
        elif sucursal == "PIEDRAS NEGRAS":
            return "Servicio Piedras Negras"
        elif sucursal == "POZA RICA":
            return "Servicio Poza Rica"
        elif sucursal == "REYNOSA":
            return "Servicio Reynosa"
        return ""
        
    def clasificacion_taller_movil(self, sucursal):
        if sucursal == "NUEVO LAREDO (AEROPUERTO)":
            return "Taller Movil", "TM NL Aereopuerto"
        if sucursal == "NUEVO LAREDO (MATRIZ)":
            return "Taller Movil", "TM NL Matriz"
        if sucursal == "MATAMOROS":
            return "Taller Movil", "TM Matamoros"
        if sucursal == "PIEDRAS NEGRAS":
            return "Taller Movil", "TM Piedras Negras"
        if sucursal == "REYNOSA":
            return "Taller Movil", "TM Reynosa"
    
    def clasificacion_area(self, departamento_venta, departamento_detalle):
        if departamento_detalle == "REFACCIONES":
            return "Null"
        elif departamento_detalle == "TALLER DE SERVICIO" and departamento_venta == "Taller Movil":
            return "MO Taller Movil"
        elif departamento_detalle == "TALLER DE SERVICIO" and departamento_venta == "Servicio":
            return "MO Servicio"



class VentasServicioKWRB:
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioRioBravo

        self.variables = Variables()
        self.nombre_doc = 'VSR.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        tipo_servicio_taller_movil = ["TM", "Taller Movil"]
        
        df.insert(
            loc=5,
            column='Fecha Hoy',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=False
        )

        self.numero_orden = 'OS' + df["Número Orden"].astype(str).str.split(".").str[0]

        self.unidad = 'UN-' + df["Unidad"].astype(str)

        df['Número Orden'] = self.numero_orden
        df["Unidad"] = self.unidad
        EXCLUDE_COLUMN_DATE = ["edo. docto. fecha"]
        COLUMNS_DATE = [col for col in df.columns 
                        if "fecha" in col.lower() and col.lower().strip() not in EXCLUDE_COLUMN_DATE
                        ]

        df["Departamento Venta"] = "Servicio"
        df["Departamento"] = ""
        df["Departamento"] = df.apply(lambda fila: self.clasificacion_servicio(fila["Sucursal"]), axis=1)
        pattern = "|".join(tipo_servicio_taller_movil)
        df[["Departamento Venta", "Departamento"]] = df.apply(
            lambda fila: (
                self.clasificacion_taller_movil(fila["Sucursal"]) 
                if pd.Series(str(fila["Tipo Servicio"])).str.contains(pattern, case=False, regex=True).any()
                else [fila["Departamento Venta"], fila["Departamento"]]
            ),
            axis=1,
            result_type="expand"
        )

        for column_name in COLUMNS_DATE:
            df = self.variables.global_date_format_america(df, column_name)
            df = self.variables.global_date_format_dmy_mexican(df, column_name)
            
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)
        df = df.astype(object).fillna("")

        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)

    def clasificacion_servicio(self, sucursal = None):
        if sucursal == "MATAMOROS":
            return "Servicio Matamoros"
        elif sucursal == "NUEVO LAREDO (AEROPUERTO)":
            return "Servicio NL Matriz"
        elif sucursal == "NUEVO LAREDO (MATRIZ)":
            return "Servicio NL Matriz"
        elif sucursal == "PIEDRAS NEGRAS":
            return "Servicio Piedras Negras"
        elif sucursal == "POZA RICA":
            return "Servicio Poza Rica"
        elif sucursal == "REYNOSA":
            return "Servicio Reynosa"
        return ""

    def clasificacion_taller_movil(self, sucursal):
        if sucursal == "NUEVO LAREDO (AEROPUERTO)":
            return "Taller Movil", "TM NL Aereopuerto"
        if sucursal == "NUEVO LAREDO (MATRIZ)":
            return "Taller Movil", "TM NL Matriz"
        if sucursal == "MATAMOROS":
            return "Taller Movil", "TM Matamoros"
        if sucursal == "PIEDRAS NEGRAS":
            return "Taller Movil", "TM Piedras Negras"
        if sucursal == "REYNOSA":
            return "Taller Movil", "TM Reynosa"
