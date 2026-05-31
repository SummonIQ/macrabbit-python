from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QGroupBox, QScrollArea,
                             QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import subprocess
import os
import shlex

def run_with_admin_privileges(cmd):
    """Run a shell command with admin privileges using osascript for a native password prompt."""
    cmd_str = ' '.join(shlex.quote(str(c)) for c in cmd)
    osa_cmd = [
        'osascript',
        '-e', f'do shell script "{cmd_str}" with administrator privileges'
    ]
    return subprocess.run(osa_cmd, capture_output=True, text=True)

class OptimizationWorker(QThread):
    """Worker thread for running optimization commands."""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, optimizations):
        super().__init__()
        self.optimizations = optimizations
    
    def run(self):
        try:
            for i, (name, commands) in enumerate(self.optimizations):
                self.progress.emit(f"Applying {name}...")
                for cmd in commands:
                    # Use admin privileges for system-level commands
                    if cmd.startswith('sudo') or 'system/' in cmd or 'mdutil' in cmd or 'defaults write /Library' in cmd:
                        # Remove 'sudo' if present, since osascript will prompt
                        cmd_parts = shlex.split(cmd)
                        if cmd_parts[0] == 'sudo':
                            cmd_parts = cmd_parts[1:]
                        result = run_with_admin_privileges(cmd_parts)
                    else:
                        import subprocess
                        result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
                    if result.returncode != 0:
                        self.finished.emit(False, f"Error running '{cmd}': {result.stderr.strip()}")
                        return
            self.finished.emit(True, "All optimizations applied successfully!")
        except Exception as e:
            self.finished.emit(False, str(e))

class QuickOptimizationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.optimization_status = {}
        self.is_dark_mode = self.detect_dark_mode()
        self.init_ui()
        self.check_all_optimizations()
        self.apply_theme()
    
    def detect_dark_mode(self):
        """Detect if macOS is in dark mode."""
        try:
            import subprocess
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() == 'Dark'
        except:
            return False
    
    def apply_theme(self):
        """Apply theme based on system preference."""
        if self.is_dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        pass  # No-op, theming is global
    
    def apply_light_theme(self):
        pass  # No-op, theming is global
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        # Header with back button
        header_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedSize(100, 36)
        self.back_btn.setStyleSheet('border-radius: 8px; background: #444; color: #f0f0f0; font-weight: 500;')
        self.back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_btn)
        header_layout.addStretch()
        title = QLabel("Quick Optimization")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size: 22px; font-weight: bold; letter-spacing: 0.5px; color: #f0f0f0;')
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        # Main content layout
        layout = QVBoxLayout()
        desc = QLabel("Select optimizations to apply. These changes will improve performance and privacy.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet('color: #b0b0b0; margin-bottom: 20px; font-size: 15px;')
        desc.setWordWrap(True)
        layout.addWidget(desc)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        self.optimizations = {}
        # Optimization groups
        self.optimization_definitions = [
            ("Touch Bar", "Disable Touch Bar services to save battery and improve performance", "touchbar", [
                "launchctl bootout system/com.apple.touchbarserver",
                "launchctl disable system/com.apple.touchbarserver"
            ]),
            ("Siri & Dictation", "Disable Siri and related services for privacy and performance", "siri", [
                "launchctl bootout system/com.apple.sirid",
                "launchctl disable system/com.apple.sirid",
                "launchctl bootout system/com.apple.siriknowledged",
                "launchctl disable system/com.apple.siriknowledged",
                "launchctl bootout system/com.apple.siriactionsd",
                "launchctl disable system/com.apple.siriactionsd"
            ]),
            ("Spotlight", "Disable Spotlight indexing for better performance", "spotlight", [
                "sudo mdutil -a -i off",
                "sudo launchctl bootout system/com.apple.metadata.mds",
                "sudo launchctl disable system/com.apple.metadata.mds"
            ]),
            ("UI Enhancements", "Disable animations and transparency for better performance", "ui", [
                "defaults write com.apple.dock expose-animation-duration -float 0.1",
                "defaults write com.apple.dock autohide-delay -float 0",
                "defaults write com.apple.dock autohide-time-modifier -float 0.1",
                "defaults write -g NSWindowResizeTime -float 0.001",
                "defaults write -g NSAutomaticWindowAnimationsEnabled -bool false",
                "defaults write com.apple.finder DisableAllAnimations -bool true",
                "defaults write -g com.apple.menu.fullWidth -bool true",
                "defaults write com.apple.universalaccess reduceTransparency -bool true"
            ]),
            ("Dock Optimizations", "Optimize dock behavior and appearance", "dock", [
                "defaults write com.apple.dock minimize-to-application -bool true",
                "defaults write com.apple.dock show-recents -bool false",
                "defaults write com.apple.dock showhidden -bool true",
                "defaults write com.apple.dock tilesize -int 48"
            ]),
            ("Advertising & Analytics", "Disable Apple's advertising and analytics services", "ads", [
                "launchctl bootout system/com.apple.adid",
                "launchctl disable system/com.apple.adid",
                "launchctl bootout system/com.apple.analyticsd",
                "launchctl disable system/com.apple.analyticsd",
                "launchctl bootout system/com.apple.ap.adprivacyd",
                "launchctl disable system/com.apple.ap.adprivacyd"
            ]),
            # New optimizations from script
            ("Clear System Caches", "Free up memory by clearing system caches (requires restart for full effect)", "clear_caches", [
                "sudo purge"
            ]),
            ("Clear DNS Cache", "Flush DNS cache to resolve network issues", "clear_dns", [
                "sudo dscacheutil -flushcache",
                "sudo killall -HUP mDNSResponder"
            ]),
            ("Clear Font Caches", "Remove and reset font caches to fix font issues", "clear_fonts", [
                "sudo atsutil databases -remove",
                "sudo atsutil server -shutdown",
                "sudo atsutil server -ping"
            ]),
            ("Clear Application Caches", "Delete app caches to free up disk space (user only)", "clear_app_caches", [
                "rm -rf ~/Library/Caches/*"
            ]),
            ("Clear Temporary Files", "Delete temporary files to free up disk space (system-wide)", "clear_tmp", [
                "rm -rf /tmp/*"
            ]),
            ("Clear Browser Caches", "Delete Chrome and Firefox caches (browsers must be closed)", "clear_browser_caches", [
                "rm -rf ~/Library/Application\ Support/Google/Chrome/Default/Cache/*",
                "rm -rf ~/Library/Application\ Support/Google/Chrome/Default/Code\ Cache/*",
                "rm -rf ~/Library/Application\ Support/Firefox/Profiles/*/cache2/*"
            ]),
            ("Stop Time Machine Backup", "Stop any running Time Machine backup", "stop_tm", [
                "sudo tmutil stopbackup"
            ]),
            ("Stop Spotlight Indexing", "Temporarily stop Spotlight indexing for performance", "stop_spotlight", [
                "sudo mdutil -a -i off"
            ]),
            ("Kill Heavy Browser Processes", "Kill Chrome/Firefox/WebKit processes to free up RAM (browsers must be closed)", "kill_browser_procs", [
                "pkill -f 'Google Chrome Helper'",
                "pkill -f 'Google Chrome GPU'",
                "pkill -f 'com.apple.WebKit.WebContent'"
            ]),
            ("Show System Status", "Show memory, disk, and CPU usage", "show_status", [
                "vm_stat | head -5",
                "df -h / | tail -1",
                "top -l 1 -n 0 | grep 'CPU usage'"
            ]),
        ]
        for title, description, key, commands in self.optimization_definitions:
            group = self.create_optimization_group(title, description, key, commands)
            scroll_layout.addWidget(group)
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply Selected Optimizations")
        self.apply_btn.setFixedSize(220, 40)
        self.apply_btn.setStyleSheet('border-radius: 8px; background: #2563eb; color: #fff; font-weight: 600; font-size: 15px;')
        self.apply_btn.clicked.connect(self.apply_optimizations)
        button_layout.addWidget(self.apply_btn)
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.setFixedSize(110, 40)
        self.select_all_btn.setStyleSheet('border-radius: 8px; background: #444; color: #f0f0f0; font-weight: 500;')
        self.select_all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(self.select_all_btn)
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setFixedSize(110, 40)
        self.clear_btn.setStyleSheet('border-radius: 8px; background: #444; color: #f0f0f0; font-weight: 500;')
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        main_layout.addLayout(layout)
        self.setLayout(main_layout)
    
    def create_optimization_group(self, title, description, key, commands):
        group = QGroupBox()
        group.setStyleSheet('QGroupBox { border-radius: 12px; border: 1px solid #444; background: #232323; margin-top: 12px; }')
        layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setFixedWidth(36)
        # Placeholder for icons, can be replaced with QPixmap icons
        icon_label.setPixmap(QPixmap())
        layout.addWidget(icon_label)
        vbox = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet('font-size: 17px; font-weight: 600; color: #f0f0f0;')
        vbox.addWidget(title_label)
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet('color: #b0b0b0; margin-bottom: 10px; font-size: 13px;')
        vbox.addWidget(desc_label)
        # macOS-style switch (styled QCheckBox)
        switch = QCheckBox()
        switch.setStyleSheet('QCheckBox::indicator { width: 44px; height: 28px; border-radius: 14px; background: #444; } QCheckBox::indicator:checked { background: #34c759; }')
        switch.setText("")
        vbox.addWidget(switch)
        # Status label
        status_label = QLabel("")
        status_label.setStyleSheet('font-size: 13px; color: #34c759; font-weight: 500;')
        vbox.addWidget(status_label)
        layout.addLayout(vbox)
        group.setLayout(layout)
        self.optimizations[key] = {
            'switch': switch,
            'commands': commands,
            'status_label': status_label,
            'group': group
        }
        return group
    
    def check_all_optimizations(self):
        for title, description, key, commands in self.optimization_definitions:
            self.check_optimization_status(key)
    
    def check_optimization_status(self, key):
        # System checks for each optimization
        import subprocess
        status = False
        if key == "touchbar":
            # Check if touchbarserver is disabled and not running
            try:
                out = subprocess.run(["sudo", "launchctl", "print-disabled", "system"], capture_output=True, text=True)
                disabled = f'"com.apple.touchbarserver" => disabled' in out.stdout
                out2 = subprocess.run(["sudo", "launchctl", "list"], capture_output=True, text=True)
                not_running = not any("com.apple.touchbarserver" in line and not line.strip().startswith('-') for line in out2.stdout.splitlines())
                status = disabled and not_running
            except Exception:
                status = False
        elif key == "siri":
            # Check if all Siri daemons are disabled and not running
            try:
                daemons = ["com.apple.sirid", "com.apple.siriknowledged", "com.apple.siriactionsd"]
                disabled = True
                not_running = True
                out = subprocess.run(["sudo", "launchctl", "print-disabled", "system"], capture_output=True, text=True)
                for d in daemons:
                    if f'"{d}" => disabled' not in out.stdout:
                        disabled = False
                out2 = subprocess.run(["sudo", "launchctl", "list"], capture_output=True, text=True)
                for d in daemons:
                    if any(d in line and not line.strip().startswith('-') for line in out2.stdout.splitlines()):
                        not_running = False
                status = disabled and not_running
            except Exception:
                status = False
        elif key == "spotlight":
            try:
                out = subprocess.run(["mdutil", "-a", "-s"], capture_output=True, text=True)
                indexing_off = all("Indexing disabled" in line for line in out.stdout.splitlines() if line.strip())
                out2 = subprocess.run(["sudo", "launchctl", "print-disabled", "system"], capture_output=True, text=True)
                disabled = f'"com.apple.metadata.mds" => disabled' in out2.stdout
                status = indexing_off and disabled
            except Exception:
                status = False
        elif key == "ui":
            try:
                # Check a few defaults values
                out = subprocess.run(["defaults", "read", "-g", "NSAutomaticWindowAnimationsEnabled"], capture_output=True, text=True)
                animations_off = out.stdout.strip() == "0" or out.stdout.strip().lower() == "false"
                out2 = subprocess.run(["defaults", "read", "com.apple.universalaccess", "reduceTransparency"], capture_output=True, text=True)
                transparency = out2.stdout.strip() == "1" or out2.stdout.strip().lower() == "true"
                status = animations_off and transparency
            except Exception:
                status = False
        elif key == "dock":
            try:
                out = subprocess.run(["defaults", "read", "com.apple.dock", "show-recents"], capture_output=True, text=True)
                show_recents = out.stdout.strip() == "0" or out.stdout.strip().lower() == "false"
                out2 = subprocess.run(["defaults", "read", "com.apple.dock", "minimize-to-application"], capture_output=True, text=True)
                minimize = out2.stdout.strip() == "1" or out2.stdout.strip().lower() == "true"
                status = show_recents and minimize
            except Exception:
                status = False
        elif key == "ads":
            try:
                daemons = ["com.apple.adid", "com.apple.analyticsd", "com.apple.ap.adprivacyd"]
                disabled = True
                not_running = True
                out = subprocess.run(["sudo", "launchctl", "print-disabled", "system"], capture_output=True, text=True)
                for d in daemons:
                    if f'"{d}" => disabled' not in out.stdout:
                        disabled = False
                out2 = subprocess.run(["sudo", "launchctl", "list"], capture_output=True, text=True)
                for d in daemons:
                    if any(d in line and not line.strip().startswith('-') for line in out2.stdout.splitlines()):
                        not_running = False
                status = disabled and not_running
            except Exception:
                status = False
        # Update UI
        opt = self.optimizations[key]
        if status:
            opt['switch'].setChecked(True)
            opt['switch'].setEnabled(False)
            opt['status_label'].setText("Already Optimized ✓")
            opt['status_label'].setStyleSheet('font-size: 13px; color: #34c759; font-weight: 500;')
        else:
            opt['switch'].setChecked(False)
            opt['switch'].setEnabled(True)
            opt['status_label'].setText("")
    
    def select_all(self):
        for opt in self.optimizations.values():
            if opt['switch'].isEnabled():
                opt['switch'].setChecked(True)
    
    def clear_all(self):
        for opt in self.optimizations.values():
            if opt['switch'].isEnabled():
                opt['switch'].setChecked(False)
    
    def apply_optimizations(self):
        selected = []
        for key, opt in self.optimizations.items():
            if opt['switch'].isChecked() and opt['switch'].isEnabled():
                selected.append((key, opt['commands']))
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select at least one optimization to apply.")
            return
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Optimizations")
        msg.setText(f"Apply {len(selected)} optimization(s)?\n\nThis may require administrator privileges.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.apply_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(selected))
            self.progress_bar.setValue(0)
            self.worker = OptimizationWorker(selected)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.optimization_finished)
            self.worker.start()
    
    def update_progress(self, message):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
    
    def optimization_finished(self, success, message):
        self.apply_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_all()
            self.check_all_optimizations()
        else:
            QMessageBox.critical(self, "Error", message)
            self.check_all_optimizations()
    
    def go_back(self):
        """Return to welcome screen."""
        # This will be handled by the main window
        pass 