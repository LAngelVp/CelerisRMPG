import sys
import os

from PyQt6.QtWidgets import QApplication
# 'InicioSesion' ya debe estar ofuscado como InicioSesion.pyd en la misma carpeta
try:
    from InicioSesion import InicioSesion 
except ImportError as e:
    # Esto ayuda a depurar si el .pyd tiene problemas de dependencias
    sys.exit(1)

def main():
    app = QApplication(sys.argv)
    login_window = InicioSesion()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()