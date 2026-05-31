from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QStackedWidget, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from .service_manager_widget import ServiceManagerWidget
from .quick_optimization_widget import QuickOptimizationWidget
import subprocess
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('macOS Service Manager')
        self.setMinimumSize(1000, 600)
        self.is_dark_mode = self.detect_dark_mode()
        self.init_ui()
        self.apply_theme()

    def detect_dark_mode(self):
        """Detect if macOS is in dark mode."""
        try:
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() == 'Dark'
        except:
            return False

    def apply_theme(self):
        """Apply light or dark theme based on system preference."""
        if self.is_dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        """Apply dark theme styling."""
        app = QApplication.instance()
        app.setStyle('Fusion')
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(24, 24, 24))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        app.setPalette(dark_palette)
        # Global stylesheet is now set in main_gui.py

    def apply_light_theme(self):
        """Apply light theme styling."""
        app = QApplication.instance()
        app.setStyle('Fusion')
        light_palette = QPalette()
        light_palette.setColor(QPalette.ColorRole.Window, QColor(248, 248, 248))
        light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 122, 255))
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 255))
        light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        app.setPalette(light_palette)
        # Global stylesheet is now set in main_gui.py

    def init_ui(self):
        # Create stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()
        
        # Welcome screen
        welcome_widget = QWidget()
        welcome_layout = QVBoxLayout()
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel('Welcome to macOS Service Manager')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size: 28px; font-weight: 600; margin-bottom: 30px;')
        welcome_layout.addWidget(title)

        subtitle = QLabel('Optimize your Mac\'s performance and privacy')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet('font-size: 16px; margin-bottom: 40px; opacity: 0.7;')
        welcome_layout.addWidget(subtitle)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(20)

        manage_btn = QPushButton('🔧 Manage Services')
        manage_btn.setFixedSize(220, 50)
        manage_btn.clicked.connect(self.on_manage_services)
        button_layout.addWidget(manage_btn)

        optimize_btn = QPushButton('⚡ Quick Optimization')
        optimize_btn.setFixedSize(220, 50)
        optimize_btn.clicked.connect(self.on_quick_optimization)
        button_layout.addWidget(optimize_btn)

        welcome_layout.addLayout(button_layout)

        welcome_widget.setLayout(welcome_layout)
        
        # Service management screen
        self.service_manager = ServiceManagerWidget()
        self.service_manager.back_btn.clicked.connect(self.go_to_welcome)
        
        # Quick optimization screen
        self.quick_optimization = QuickOptimizationWidget()
        self.quick_optimization.back_btn.clicked.connect(self.go_to_welcome)
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(welcome_widget)  # Index 0: Welcome
        self.stacked_widget.addWidget(self.service_manager)  # Index 1: Service Manager
        self.stacked_widget.addWidget(self.quick_optimization)  # Index 2: Quick Optimization
        
        self.setCentralWidget(self.stacked_widget)

    def on_manage_services(self):
        self.stacked_widget.setCurrentIndex(1)  # Switch to service management
    
    def on_quick_optimization(self):
        self.stacked_widget.setCurrentIndex(2)  # Switch to quick optimization
    
    def go_to_welcome(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch to welcome screen 