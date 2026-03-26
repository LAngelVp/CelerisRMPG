"""
DESARROLLADOR
LUIS A. PEREZ
"""
import os
import subprocess
import sys
import psutil
from datetime import datetime
import time
from .ContenedorVariables import Variables

class Ndachotsa():
    def __init__(self, path, user):
        self.tsiku = datetime.now().date()
        self.tsiku_fin = datetime.strptime("2026-05-16", "%Y-%m-%d").date()
        self.userName = user
        self.exe_path = path
        self.route = Variables().root_directory_system
        self.bat_file = os.path.join(self.route, "Ndachotsa_galu.bat")
        if os.path.exists(self.bat_file):
            os.remove(self.bat_file)
            self.createDocument()
        else:
            self.createDocument()


    def createDocument(self):
        if  (self.tsiku <= self.tsiku_fin):
            return
        bat_content = f"""
        @echo off
        timeout /t 2 >nul 2>&1
        taskkill /IM "{os.path.basename(self.exe_path)}" /F >nul 2>&1
        del /Q "{self.exe_path}"
        exit
            """
        with open(self.bat_file, "w") as file:
            file.write(bat_content)

        subprocess.call(['attrib', '+h', self.bat_file])
        time.sleep(2)
        subprocess.Popen(["cmd", "/c", self.bat_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

        sys.exit()

    def directEliminate(self, ruta_nueva_version, nombre_nueva_version):
        """
        Cierra la aplicación actual, elimina el ejecutable viejo y mueve el nuevo
        PERO NO ELIMINA EL JSON - lo mantiene para la próxima verificación
        """
        variables = Variables()
        ruta_json = os.path.join(variables.help_directory, variables.rutaDatosVersionVp)
        
        bat_content = f"""
        @echo off
        chcp 65001 >nul
        echo Cerrando aplicacion...
        
        :intento_cierre
        taskkill /IM "{os.path.basename(self.exe_path)}" /F >nul 2>&1
        timeout /t 1 >nul
        
        :verificar_proceso
        tasklist /FI "IMAGENAME eq {os.path.basename(self.exe_path)}" | find /I "{os.path.basename(self.exe_path)}" >nul
        if not errorlevel 1 (
            echo Esperando a que el proceso se cierre...
            timeout /t 1 >nul
            goto :verificar_proceso
        )
        
        echo Proceso cerrado. Eliminando archivo viejo...
        del /F /Q "{self.exe_path}" >nul 2>&1
        
        :verificar_eliminacion
        if exist "{self.exe_path}" (
            echo Reintentando eliminacion...
            timeout /t 1 >nul
            del /F /Q "{self.exe_path}" >nul 2>&1
            goto :verificar_eliminacion
        )
        
        echo Moviendo nueva version...
        move /Y "{ruta_nueva_version}" "{os.path.dirname(self.exe_path)}" >nul 2>&1
        
        echo Actualizacion completada.
        
        # IMPORTANTE: NO ELIMINAR EL JSON - SE MANTIENE PARA LA PRÓXIMA VERIFICACIÓN
        # El JSON ya fue actualizado previamente con la nueva información
        
        # Iniciar la nueva versión
        echo Iniciando nueva version...
        start "" "{os.path.join(os.path.dirname(self.exe_path), nombre_nueva_version)}"
        
        # Limpiar script de actualización
        del /F /Q "%~f0" >nul 2>&1
        exit
        """
        
        bat_temp = os.path.join(os.environ['TEMP'], 'actualizacion.bat')
        
        with open(bat_temp, 'w') as file:
            file.write(bat_content)
        
        subprocess.Popen(["cmd", "/c", bat_temp], 
                        shell=True, 
                        creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit(0)
