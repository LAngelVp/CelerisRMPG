"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class Compras(Variables):
    def __init__(self):
        super().__init__() # Importante llamar al super para heredar correctamente
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
        self.nombre_doc = 'CDR.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwrb, self.nombre_doc)
        
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df2 = df.copy()

        # 1. Aseguramos que Fecha_Hoy sea operable como datetime
        df2["Fecha_Hoy"] = pd.to_datetime(self.variables.date_movement_config_document(), errors='coerce')

        # 2. Convertimos columnas de fecha de forma segura
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_america(df2, column_name)
                # Forzamos conversión a datetime de Pandas para poder restar
                df2[column_name] = pd.to_datetime(df2[column_name], errors='coerce')

        # 3. Operaciones de resta (Soportan NaT)
        antiguedad = (df2['Fecha Captura'] - df2['Fecha Docto.'])
        antiguedad_factura = (df2['Fecha_Hoy'] - df2['Fecha Docto.'])

        # 4. Inserción de columnas
        df2.insert(loc=7, column='Antigüedad', value=antiguedad, allow_duplicates=False)
        df2.insert(loc=8, column='Antigüedad Fact', value=antiguedad_factura, allow_duplicates=False)

        # 5. Conversión a días y limpieza de errores (NaT -> 0)
        # Reemplazamos el .apply() por lógica nativa de Pandas (más rápido)
        df2["Antigüedad"] = df2["Antigüedad"].dt.days.fillna(0).astype(int).clip(lower=0)
        df2["Antigüedad Fact"] = df2["Antigüedad Fact"].dt.days.fillna(0).astype(int).clip(lower=0)

        # 6. Limpieza y formato final
        df2.drop(['Folio', 'Fecha_Hoy'], axis=1, inplace=True)
        
        columnas_bol = df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)
        
        for column_name in df2.columns:
            if "fecha" in column_name.lower():
                df2 = self.variables.global_date_format_mdy_america(df2, column_name)

        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)

    # Nota: Ya no necesitas 'convertir_a_cero' porque .clip(lower=0) hace el trabajo