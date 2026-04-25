import sys
import os
import traceback

# Configuración para que el .exe encuentre sus propios archivos internos
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from PyQt6.QtWidgets import QApplication

try:
    from InicioSesion import InicioSesion 
except ImportError as e:
    # ESTO TE MOSTRARÁ EL ERROR REAL EN LA CONSOLA
    print(f"ERROR CRÍTICO AL IMPORTAR InicioSesion: {e}")
    traceback.print_exc()
    input("Presiona ENTER para salir...") # Mantiene la consola abierta para que leas el error
    sys.exit(1)
except Exception as e:
    print(f"OTRO ERROR: {e}")
    traceback.print_exc()
    input("Presiona ENTER para salir...")
    sys.exit(1)

def main():
    app = QApplication(sys.argv)
    login_window = InicioSesion()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()