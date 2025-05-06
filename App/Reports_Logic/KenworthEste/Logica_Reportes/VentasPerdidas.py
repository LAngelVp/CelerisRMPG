import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
import locale
from time import sleep

class VentasPerdidas(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.lista_sucursales_refacciones = []
        self.lista_sucursales_servicio = []
        self.df_final = pd.DataFrame()

        self.documentos_ventasperdidas_sucursal = [
            "VPMATRIZ.xls",
            "VPTREBOL.xls",
            "VPVERACRUZ.xls",
            "VPORIZABA.xls",
            "VPTEHUACAN.xls",
            "VPVILLAHERMOSA.xls",
            "VPCOATZACOALCOS.xls",
            "VPMERIDA.xls",
            "VPOAXACA.xls",
            "VPTUXTLA1.xls",
            "VPTUXTLA2.xls",
        ]
        
        # Asegúrate de que 'ruta_ventasperdidas' sea una propiedad de la clase
        self.ruta_ventasperdidas = None
        # Obtener la ruta base donde se almacenan los archivos
        self.ruta_base = self.variables.ruta_Trabajos_kwe
        
    def comprobar_existencia_ventasperdidas(self):
        # Buscar si ya existe un archivo con ventas perdidas
        self.df_final = None  # Inicializamos en None
        for ventasperdidas in os.listdir(self.variables.ruta_exitosos_kwe):
            if "ventasperdidas" in ventasperdidas:
                self.ruta_ventasperdidas = os.path.join(self.variables.ruta_exitosos_kwe, ventasperdidas)
                break  # Solo tomamos el primero que encontremos

        if self.ruta_ventasperdidas and os.path.exists(self.ruta_ventasperdidas):
            self.df_final = pd.read_excel(self.ruta_ventasperdidas)
            print("Archivo 'ventasperdidas.xls' encontrado y cargado.")
            
    def venta_perdida_matriz(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPMATRIZ.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_trebol(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTR  EBOL.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_veracruz(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPVERACRUZ.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_orizaba(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPORIZABA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_tehuacan(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTEHUACAN.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_villahermosa(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPVILLAHERMOSA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_coatzacoalcos(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPCOATZACOALCOS.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_merida(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPMERIDA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_oaxaca(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPOAXACA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_tuxtla1(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTUXTLA1.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_tuxtla2(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTUXTLA2.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def comprobar_documento(self, documento):
        ruta_completa = os.path.join(self.ruta_base, documento)

        # Verificar si el archivo fuente existe
        if not os.path.exists(ruta_completa):
            print(f"El documento {documento} no existe.")
            return

        df = self.proceso(documento)
        if df is None:
            return
        # Determinar si hay departamentos y construir fila extra
        refacciones = df.loc[df["Departamento"] == "Refacciones", "Departamento"].head(1).iloc[0] if not df[df["Departamento"] == "Refacciones"].empty else None
        servicio = df.loc[df["Departamento"] == "Servicio", "Departamento"].head(1).iloc[0] if not df[df["Departamento"] == "Servicio"].empty else None
        sucursal = df["Sucursal"].iloc[0]

        print(f"DEPAS: {refacciones, servicio}")
        fila_extra = self.creacion_filas_en_cero(sucursal, refacciones=refacciones, servicio=servicio)

        # Concatenar nueva info con fila (si hay) y documento original
        df_nuevo = pd.concat([fila_extra, df], ignore_index=True) if not fila_extra.empty else df

        # Concatenar sobre el DataFrame global
        if self.df_final is None:
            self.df_final = df_nuevo  # primera vez
        else:
            self.df_final = pd.concat([self.df_final, df_nuevo], ignore_index=True)

        print(f"documento concatenado: {documento}")
        
    def proceso(self, nombre_documento):
        self.nombre_doc = nombre_documento
        path = os.path.join(self.variables.ruta_Trabajos_kwe, self.nombre_doc)

        # Leer el archivo Excel
        df = pd.read_excel(path, sheet_name=0)

        if df.empty:
            return None

        # Reemplazar los puntos y comas por guiones
        df = df.replace(to_replace=";", value="-", regex=True)
        df = df.drop(df.index[-1])  # Eliminar la última fila

        # Convertir la columna "Hora" a formato adecuado
        hora = pd.to_datetime(df["Hora"])
        df["Hora"] = hora.dt.strftime('%I:%M:%S %p').astype(str)

        # Procesar las columnas de fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)

        df["Mes"] = df["Fecha"].apply(lambda x:self.variables.nombre_mes_completo_base_columna(x))
        
        df["Año"] = df["Fecha"].apply(lambda x:self.variables.nombre_año_completo_base_columna(x))
        
        df.insert(0, "VP", 1, allow_duplicates=False)

        # Concatenar la columna "Venta Perdida"
        col_venta_perdida_concat = "VP-" + df["Venta Perdida"].astype(int).astype(str)
        df["Venta Perdida"] = col_venta_perdida_concat

        # Cargar la información de vendedores
        vendedores = pd.read_json(os.path.join(self.variables.help_directory, "VendedoresVP.json"))
        df.insert(12, column="Departamento", value="", allow_duplicates=False)

        # Mapear los departamentos
        df["Departamento"] = df['Usuario'].map(vendedores.set_index('Usuario')['Departamento'])

        # Reconvertir las fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_dmy_mexican(df, column_name)

        # Convertir columnas booleanas a texto
        columnas_bol = df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)
        
        return df

    def creacion_filas_en_cero(self, sucursal, refacciones=None, servicio=None):
        def crear_fila(departamento):
            fecha = Variables().date_movement_config_document()
            return pd.DataFrame({
                "VP": [0],
                "Venta Perdida": ["-"],
                "Id. Cliente": [0],
                "Nombre Cliente": ["-"],
                "Núm. Artículo": ["-"],
                "Artículo": ["-"],
                "Motivo": ["NO EXIST EN SUCURSAL (MOVTO)"],
                "Cantidad": [0],
                "Fecha": [fecha],
                "Hora": [fecha],
                "Comentario": ["-"],
                "Usuario": ["-"],
                "Departamento": [departamento],
                "Sucursal": [sucursal],
                "Programa": ["Ventas Perdidas"],
                "Tipo de Inventario": ["Refacciones"],
                "Precio": [0],
                "Clasificación": ["E"],
                "Desc. Clasificación": ["Sin Eventos"],
                "Costo": [0],
                "Total": [0],
                "Id. Competidor": [0],
                "Competidor": ["-"],
                "Precio Competidor": [0],
                "Moneda Competidor": ["-"]
            })

        dfs = []

        # Si 'refacciones' no es None, crear la fila de "Servicio"
        if refacciones and not servicio:
            fila_servicio = crear_fila("Servicio")
            dfs.append(fila_servicio)

        # Si 'servicio' no es None, crear la fila de "Refacciones"
        elif servicio and not refacciones:
            fila_refacciones = crear_fila("Refacciones")
            dfs.append(fila_refacciones)

        # Si ambos son None, no se crean filas
        elif refacciones and servicio:
            return pd.DataFrame()  # No crear ninguna fila si ambos están presentes

        # Si se generaron filas, concatenarlas y devolver el resultado
        if dfs:
            fila_dataframe = pd.concat(dfs, ignore_index=True)
            fila_dataframe["Mes"] = fila_dataframe["Fecha"].apply(lambda x:self.variables.nombre_mes_completo_base_columna(x))
            fila_dataframe["Año"] = fila_dataframe["Fecha"].apply(lambda x:self.variables.nombre_año_completo_base_columna(x))
            hora = pd.to_datetime(fila_dataframe["Hora"])
            fila_dataframe["Hora"] = hora.dt.strftime('%I:%M:%S %p').astype(str)
            for column_name in fila_dataframe.columns:
                if "fecha" in column_name.lower():
                    fila_dataframe = self.variables.global_date_format_dmy_mexican(fila_dataframe, column_name)
            return fila_dataframe

        return pd.DataFrame()  # Si no se generaron filas, devolver un DataFrame vacío
    
    def guardar_todo(self):
        if not self.df_final.empty:
            self.variables.guardar_xls("ventasperdidas.xls", self.df_final, self.concesionario)
            print("Archivo final de ventas perdidas guardado correctamente.")
        else:
            print("No hay datos para guardar.")