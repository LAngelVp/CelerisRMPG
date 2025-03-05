#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class ServicioDetallado(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
        # array_columns = ['ObjRefacc','ObjUBTRef','ObjMO', 'ObjUTBMO','Clasificacion Cliente']
        array_Garantia = ["KENWORTH MEXICANA", "PACCAR PARTS MEXICO", "DISTRIBUIDORA MEGAMAK"]
        array_PLM = ["PACCAR FINANCIAL MEXICO", "PACLEASE MEXICANA"]
        
        self.json_vendedores = self.variables.vendedores_y_depas_este_servicio_sonora()

        self.nombre_doc = "SDS.xlsx"
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        pt = pd.read_excel(path, sheet_name='Hoja2')
        pt = pt.replace(to_replace=';', value='-', regex=True)
        df = pt.copy()

        df.insert(
            loc=5,
            column='Fecha_Movimiento',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=True
        )
        df.insert(
            loc=6,
            column='Mes',
            value= self.variables.nombre_mes(),
            allow_duplicates=True
        )

        df.insert(3,"Clasificacion Cliente","CLIENTES GENERALES",allow_duplicates=False)

        df["Cliente"].fillna("", inplace=True)
        #CLASIFICACION DEL CLIENTE (NORMAL)
        df.loc[df["Cliente"].str.contains("KENWORTH") & ~df["Cliente"].str.contains("KENWORTH MEXICANA") & ~df["Cliente"].str.contains("KENWORTH DISTRIBUIDORA DE SONORA"), "Clasificacion Cliente"] = "CONCESIONARIOS"
        df.loc[df["Cliente"].str.contains("|".join(array_Garantia)),"Clasificacion Cliente"] = "GARANTIA"
        df.loc[df["Cliente"].str.contains("|".join(array_PLM)),"Clasificacion Cliente"] = "PLM"
        df.loc[(df["Cliente"] == "KENWORTH DISTRIBUIDORA DE SONORA") | (df["Cliente"] == ""), "Clasificacion Cliente"] = "CI"
        df.loc[(df["Cliente"].str.contains("SEGUROS")) | (df["Cliente"].str.contains("SEGURO")) | (df["Cliente"] == "GRUPO NACIONAL PROVINCIAL"), "Clasificacion Cliente"] = "SEGUROS"
        
        df["Unidad"].fillna("",inplace=True)
        unidad = "UN-" + df["Unidad"].map(str)
        numero_orden = 'OS' + df["Número Orden"].astype(str).str.split(".").str[0].replace("nan","").fillna("")
        
        df["Unidad"] = unidad
        df["Número Orden"] = numero_orden

        df[["Depa Venta", "Depa"]] = df.apply(
            lambda fila: pd.Series(self.obtener(fila["Vendedor"])), axis=1
        )
        
        #COMMENT: MOVEMOS LAS COLUMNAS DE DEPARTAMENTO
        columna_depaventa = df.pop("Depa Venta")
        columna_depa = df.pop("Depa")
        df.insert(
            20,
            "Departamento Venta",
            columna_depaventa
        )
        df.insert(
            21,
            "Depa",
            columna_depa
        )

        for column_name in df.columns:
                if "fecha" in column_name.lower():
                    df = self.variables.global_date_format_america(df, column_name)
                    df = self.variables.global_date_format_dmy_mexican(df, column_name)
                else:
                    pass

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        df.drop(['Hora Docto.','Fecha Cancelación','Id. Paquete','Paquete','Descripción Paquete','Cantidad Paquete',"Subtotal Paquete",'Saldo'], axis=1, inplace=True)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)

    #COMMENT_FUNCTION: FUNCION PARA CLASIFICAR VENDEDORES EN SUS DEPARTAMENTOS
    def obtener(self, vendedor):
        for index, fila in self.json_vendedores.iterrows():
            vendedor_actual = fila["Vendedor"]
            departamento_venta = fila["Depa_Venta"]
            departamento = fila["Depa"]

            if vendedor == vendedor_actual:
                return departamento_venta, departamento

        #COMMENT: SI NO ENCUENTRA VALORES, RETORNE VACIO
        return "", ""