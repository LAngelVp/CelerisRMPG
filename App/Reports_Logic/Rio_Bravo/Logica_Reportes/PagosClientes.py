"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class PagosClientes(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()

        self.nombre_doc = 'PCR.xlsx'
        self.ruta = self.variables.customerPaymentGoals
    

        self.columnas_objetivo = []
        self.objetivos = pd.DataFrame()
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        d = df.copy()

        d.drop({'Hora Pago', 'Referencia', 'Días Plazo', 'DocumentoMSC', 'Observaciones Pago', 'Referencia Forma de Pago', 'Sucursal Responsable', 'Folio Interno Factura'}, axis=1, inplace=True)
        d.columns = d.columns.str.replace(' ', '_')

        d.insert(
            loc=4,
            column='Fecha_Movimiento',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=False
            )

        for dato in d['CuentaBancaria']:
            try:
                if (dato.isdigit() == True ):
                    continue
                else:
                    d['CuentaBancaria'] = d['CuentaBancaria'].replace(dato,0)
            except:
                pass

        x = 0
        for columnas in d:
            if (columnas == 'Sucursal_Factura' ):
                d.insert(
                loc = (x + 1),
                column = 'CLASS_SUCURSAL',
                value = 'OTROS',
                allow_duplicates = False
                )
                break
            else:
                pass
            x = x + 1

        d['Objetivo'] = 0

        credito = d["Forma_Pago_Factura"] == "Crédito"
        contado = d["Forma_Pago_Factura"] == "Contado"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Tipo_Docto."] == "Nota de cargo"),
            "CLASS_SUCURSAL",
        ] = "12 NOTA DE CARGO"
        d.loc[
            (credito)
            & (d["Cliente_Pago"] == "RECICLADORA INDUSTRIAL DE ACUMULADORES"),
            "CLASS_SUCURSAL",
        ] = "12 NOTA DE CARGO"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].isin(["PACLEASE MEXICANA","PACCAR FINANCIAL MEXICO"]))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "11 PACLEASE"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].str.contains("PACCAR PARTS MEXICO"))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO", "ADMINISTRACION"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "09 GARANTIAS PACCAR PARTS"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].str.contains("ALESSO"))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO", "ADMINISTRACION"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "08 ALESSO"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "DANIEL ALEJANDRO JACINTO LOPEZ")
            & (d["Cliente_Pago"].str.contains("KENWORTH MEXICANA"))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO", "ADMINISTRACION"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "07 GARANTIAS KENMEX"

        d.loc[
            (credito)
            & (d["Id_Cliente_Pago"].isin([552,799,1357,1362,1171,1170,1169,1517,557,1259,1514]))
            & (d["Tipo_Docto."] == "Factura")
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "05 CLIENTE ESPECIAL"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "GUADALUPE JUAREZ")
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "04 PIEDRAS NEGRAS"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "ELIZABETH GONZALEZ FERNANDEZ")
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "03 MATAMOROS"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"] == "ALEYDA DE LA CRUZ MENDOZA")
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "02 REYNOSA"

        d.loc[
            (credito)
            & (d["Usuario_Aplicó"].isin(["LESLY MARTINEZ MARTINEZ PARTIDA","VIVIAN IVETTE ROJO GARCIA"]))
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"]))
            & (d["CLASS_SUCURSAL"] == "OTROS"),
            "CLASS_SUCURSAL",
        ] = "01 NUEVO LAREDO"

        d.loc[
            (contado)
            & (d["Tipo_Docto."].isin(["Factura"]))
            & (d["Departamento"].isin(["REFACCIONES", "TALLER DE SERVICIO"])),
            "CLASS_SUCURSAL",
        ] = "06 CONTADO"

        data = self.fila_objetivo(d)

        for column_name in data.columns:
                if "fecha" in column_name.lower():
                    data = self.variables.global_date_format_america(data, column_name)
                    data = self.variables.global_date_format_dmy_mexican(data, column_name)
                else:
                    pass

        columnas_bol=data.select_dtypes(include=bool).columns.tolist()
        data[columnas_bol] = data[columnas_bol].astype(str)

        if os.path.exists(self.ruta):
            try:
                df_json = pd.read_json(self.ruta)
                for indice, fila in df_json.iterrows():
                    sucursal_json = fila["nombre"]
                    objetivo_json = fila["objetivo"]

                    if sucursal_json in data["CLASS_SUCURSAL"].values.tolist():
                        data.loc[data["CLASS_SUCURSAL"] == sucursal_json, "Objetivo"] = objetivo_json
                    
                    else:
                        pass
            except:
                pass
        
        data.columns = data.columns.str.replace('_', ' ')

        self.variables.guardar_datos_dataframe(self.nombre_doc, data, self.concesionario)

    def fila_objetivo(self, dataframe_completo):
        # 1. Creamos un diccionario con todas las columnas en blanco/0 por defecto
        nueva_fila = {}
        
        for col in dataframe_completo.columns:
            # Buscamos el tipo de dato original
            dtype = dataframe_completo[col].dtype
            
            # Asignación de valores según tus reglas
            if col == "Usuario_Aplicó":
                nueva_fila[col] = 'DANIA VARGAS ROSAS'
            elif col == "CLASS_SUCURSAL":
                nueva_fila[col] = 'Objetivo KWRB'
            elif col == "Departamento":
                nueva_fila[col] = 'KWRB'
            elif col == "Mes":
                nueva_fila[col] = self.variables.nombre_mes()
            elif col in ["Fecha_Pago", "Fecha_Movimiento"]:
                nueva_fila[col] = self.variables.date_movement_config_document()
            elif pd.api.types.is_numeric_dtype(dtype):
                nueva_fila[col] = 0
            else:
                nueva_fila[col] = ''

        # 2. Convertimos el diccionario a un DataFrame de una sola fila
        fila_df = pd.DataFrame([nueva_fila])

        # 3. Concatenamos. Usamos ignore_index=True para que no haya conflicto de índices
        DataFrameConObjetivo = pd.concat([dataframe_completo, fila_df], ignore_index=True)
        
        return DataFrameConObjetivo