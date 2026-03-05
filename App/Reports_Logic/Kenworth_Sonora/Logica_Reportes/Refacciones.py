"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import*
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class Refacciones(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioSonora

        self.variables = Variables()
        self.nombre_doc = 'RS.xlsx'
        self.clasificacion_vendedores_json = self.variables.clasificacion_vendedores_departamentos_refacciones_sonora()

        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)

        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df.drop(['% Margen', 'Meta Ventas Por Vendedor', 'Meta Margen Por Vendedor', 'Meta Cantidad Por Vendedor', 'Meta Ventas Por Sucursal', 'Meta Margen Por Sucursal', 'Meta Cantidad Por Sucursal', '% Comisión Por Margen', '% Comisión Por Ventas', 'Comisión Por Margen', 'Comisión Por Ventas', 'EsBonificacion', 'IdUsuario', 'IdPaquete', 'Paquete', 'Descripción Paquete', 'Cantidad Paquete', 'Subtotal Paquete', 'Potencial Total', 'Tipo de Cambio del día', 'OCCliente', '% Margen Sin Descuento'], axis=1, inplace=True)
        df= df[df.columns[0:93]].copy()
        EXCLUDE_COLUMN_DATE = ["estado factura fecha"]
        COLUMNS_DATE = [col for col in df.columns 
                        if "fecha" in col.lower() and col.lower().strip() not in EXCLUDE_COLUMN_DATE
                        ]

        df["Departamento Venta"] = ""
        df["Depa"] = ""

        df[["Departamento Venta","Depa"]] = df.apply(
            lambda fila: pd.Series(
                self.clasificacion_vendedores(fila["Vendedor"], fila["Sucursal"])
            ),
            axis=1,
        )

        for column_name in COLUMNS_DATE:
            df = self.variables.global_date_format_america(df, column_name)
            df = self.variables.global_date_format_dmy_mexican(df, column_name)
        
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
        
    def clasificacion_vendedores(self, vendedor, sucursal):
        for index, valor in self.clasificacion_vendedores_json.iterrows():
            valor_vendedor = valor["vendedor"]
            valor_sucursal = valor["sucursal"]
            valor_depto_venta = valor["depto venta"]
            valor_departamento = valor["departamento"]
            if vendedor == valor_vendedor and sucursal == valor_sucursal:
                return valor_depto_venta, valor_departamento
        return "", ""