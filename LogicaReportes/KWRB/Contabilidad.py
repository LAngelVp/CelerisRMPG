"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class ContabilidadAnalisis:
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioRioBravo
        self.variables = Variables()
    
    def anexos_moimientos_gastos(self):
        def cuentas_sucursal(cuenta, sucursales):
            try:
                clave = cuenta[5:7]  
                for _, fila in sucursales.iterrows():
                    if fila["numCuentaSucursal"] == clave:
                        return fila["sucursal"]
            except Exception:
                pass
            return None
        
        def cuentas_departamento(cuenta, departamentos):
            try:
                clave = cuenta[7:9]  
                for _, fila in departamentos.iterrows():
                    if fila["numCuentaDepartamento"] == clave:
                        return fila["departamento"]
            except Exception:
                pass
            return None
            
        self.nombre_doc = "AMR.xlsx"
        ruta = os.path.join(self.variables.ruta_Trabajos_kwrb,self.nombre_doc)
        data = pd.read_excel(ruta, sheet_name='Hoja2')
        data = data.fillna("")
        data["Mes"] = self.variables.nombre_mes()
        data["Año"] = self.variables.year_completo()
        data["Prog"] = self.variables.date_movement_config_document().month
        documento_json = pd.read_json(os.path.join(self.variables.help_directory, "anexos_movimientos_gastos.json"), typ="series")
        sucursales_frame = pd.DataFrame(documento_json["sucursales"])
        departamento_frame = pd.DataFrame(documento_json["departamentos"])
        data["Sucursal"] = data["Cuenta"].apply(lambda x: cuentas_sucursal(x, sucursales_frame))
        data["Departamento"] = data["Cuenta"].apply(lambda x: cuentas_departamento(x, departamento_frame))
        
        for column_name in data.columns:
                if "fecha" in column_name.lower():
                    data = self.variables.global_date_format_dmy_mexican(data, column_name)
                else:
                    pass
                
        self.variables.guardar_datos_dataframe(self.nombre_doc, data, self.concesionario)