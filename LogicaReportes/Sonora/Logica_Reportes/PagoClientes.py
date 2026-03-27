"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class PagosDeClientes(Variables):
    def __init__(self) -> None:
        super().__init__()
        
        self.variables = Variables()
        self.concesionario = Concesionarios().concesionarioSonora
        
        self.nombre_doc = 'PCS.xlsx'
        self.ruta = self.variables.customerPaymentGoals
        path = os.path.join(self.variables.ruta_Trabajos_kwsonora,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        df.drop({'Hora Pago', 'Referencia', 'Días Plazo', 'DocumentoMSC', 'Observaciones Pago', 'Referencia Forma de Pago', 'Sucursal Responsable', 'Folio Interno Factura'}, axis=1, inplace=True)
        df = df.rename(columns={'Tipo Docto.':'Tipo Docto'})

        df.columns = df.columns.str.replace(' ', '_')

        df.insert(
            loc=4,
            column='Fecha_Movimiento',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=True
        )
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)
                df = self.variables.global_date_format_dmy_mexican(df, column_name)
            else:
                pass
        
        for dato in df['CuentaBancaria']:
            try:
                if (dato.isdigit() == True ):
                    continue
                else:
                    df['CuentaBancaria'] = df['CuentaBancaria'].replace(dato,0)
            except:
                pass

        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)

        df.columns = df.columns.str.replace(' ', '_')
        df_completo = df.copy()
        df_completo.columns = df_completo.columns.str.replace('_', ' ')

        self.variables.guardar_datos_dataframe(self.nombre_doc, df_completo, self.concesionario)
