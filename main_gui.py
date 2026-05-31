import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.gui.main_window import MainWindow

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller/py2app """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    elif getattr(sys, 'frozen', False):
        # py2app, py2exe, cx_Freeze
        bundle_dir = os.path.abspath(os.path.dirname(sys.executable))
        return os.path.join(bundle_dir, '..', 'Resources', relative_path)
    else:
        # Development
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)

def main():
    qss_path = resource_path('theme.qss')
    with open(qss_path, 'r') as f:
        global_stylesheet = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(global_stylesheet)  # Set the global stylesheet here
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 