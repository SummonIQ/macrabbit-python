from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                             QListWidgetItem, QTextEdit, QPushButton, QLabel,
                             QSplitter, QProgressBar, QMessageBox, QFrame, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QPalette, QPainter, QBrush
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtWidgets import QApplication
import psutil

# Master list of all possible categories (update as needed)
ALL_CATEGORIES = [
    "All Categories",
    "🔍 Advertising & Analytics",
    "🛒 App & Store Related",
    "🔌 Hardware & Drivers",
    "🗣️ Siri & Dictation",
    "🔧 Other Services"
]
CATEGORY_ICONS = {
    "All Categories": "view-list-details",
    "🔍 Advertising & Analytics": "system-search",
    "🛒 App & Store Related": "applications-system",
    "🔌 Hardware & Drivers": "computer",
    "🗣️ Siri & Dictation": "microphone",
    "🔧 Other Services": "preferences-system"
}

class ServiceManagerWidget(QWidget):
    """Main service management widget with categories, services, and details."""
    
    def __init__(self):
        super().__init__()
        self.is_dark_mode = self.detect_dark_mode()
        self.setAutoFillBackground(True)
        self.setStyleSheet(self.get_main_stylesheet())
        self.categories = [
            "All Categories",
            "🔍 Advertising & Analytics",
            "🛒 App & Store Related", 
            "🔌 Hardware & Drivers",
            "🗣️ Siri & Dictation",
            "🔧 Other Services"
        ]
        
        # Load real service data
        from core.service_manager import get_live_services
        self.services_data = get_live_services()
        
        # Update categories based on available data
        self.categories = [cat for cat in self.categories if cat == "All Categories" or cat in self.services_data]
        if "🔧 Other Services" in self.services_data and "🔧 Other Services" not in self.categories:
            self.categories.append("🔧 Other Services")
        
        self.current_category = None
        self.pending_changes = {}
        self.init_ui()
    
    def detect_dark_mode(self):
        """Detect if macOS is in dark mode."""
        try:
            import subprocess
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() == 'Dark'
        except:
            return False
    
    def get_main_stylesheet(self):
        # Clean, compact, modern macOS-inspired theme with gradient background
        return (
            'QWidget { '
            '  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", Arial, sans-serif;'
            '  background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #303030, stop:1 #1a1a1a);'
            '  color: #eaeaea;'
            '  font-size: 14px;'
            '}'
            'QLabel { color: #eaeaea; font-size: 14px; }'
            'QTextEdit { background: transparent; border: none; color: #eaeaea; padding: 10px; font-size: 14px; }'
            'QListWidget { background: transparent; border: none; font-size: 14px; }'
            'QListWidget::item { padding: 6px 10px; border-radius: 8px; margin: 1px 0; }'
            'QListWidget::item:selected { background: #007aff33; border-radius: 8px; color: #fff; font-weight: 600; }'
            'QListWidget::item:hover { background: #2c2f36; }'
            'QPushButton { background: #007aff; color: #fff; border: none; border-radius: 12px; font-size: 15px; padding: 8px 28px; margin: 0; font-weight: 600; }'
            'QPushButton:disabled { background: #444; color: #aaa; }'
            'QPushButton:hover { background: #339cff; }'
            'QPushButton:pressed { background: #005bb5; }'
            'QLineEdit { border-radius: 8px; padding: 6px 10px; font-size: 14px; background: #232323; color: #fff; border: 1px solid #444; margin-bottom: 6px; }'
            'QFrame#separator { background: #333; min-width: 1px; max-width: 1px; }'
            'QScrollBar:vertical { background: transparent; width: 8px; margin: 0px 0px 0px 0px; border-radius: 4px; }'
            'QScrollBar::handle:vertical { background: #444; min-height: 16px; border-radius: 4px; }'
            'QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }'
        )
    
    def apply_panel_style(self, widget):
        # Only apply shadow and border radius, not background or color
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(12)
        effect.setOffset(0, 2)
        effect.setColor(QColor(0, 0, 0, 60 if self.is_dark_mode else 30))
        widget.setGraphicsEffect(effect)
        widget.setStyleSheet('border-radius: 12px;')
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Header with back button and apply button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 8, 16, 0)
        header_layout.setSpacing(8)
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedSize(80, 28)
        self.back_btn.setStyleSheet('QPushButton { background: transparent; color: #aaa; border: none; font-size: 13px; padding: 2px 10px; border-radius: 8px; } QPushButton:hover { background: #333; color: #fff; }')
        self.back_btn.setToolTip("Return to Welcome Screen")
        self.back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_btn)
        header_layout.addStretch()
        title = QLabel("macOS Service Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("San Francisco", 18, QFont.Weight.Bold))
        title.setStyleSheet('color: #fff; letter-spacing: 1px;')
        header_layout.addWidget(title)
        header_layout.addStretch()
        # Apply button in top right
        self.apply_btn = QPushButton('Apply Changes')
        self.apply_btn.setFixedHeight(32)
        self.apply_btn.setStyleSheet('QPushButton { background: #007aff; color: #fff; border: none; border-radius: 12px; font-size: 15px; padding: 8px 28px; font-weight: 600; } QPushButton:disabled { background: #444; color: #aaa; } QPushButton:hover { background: #339cff; } QPushButton:pressed { background: #005bb5; }')
        self.apply_btn.clicked.connect(self.apply_changes)
        header_layout.addWidget(self.apply_btn)
        main_layout.addLayout(header_layout)
        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(16, 0, 16, 0)
        content_layout.setSpacing(8)
        # Sidebar (categories)
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(4)
        self.category_list = QListWidget()
        self.category_list.setFixedWidth(220)
        self.category_list.setStyleSheet('QListWidget { background: transparent; border: none; font-size: 14px; }')
        self.category_items = []
        for cat in ALL_CATEGORIES:
            item = QListWidgetItem(cat)
            icon_name = CATEGORY_ICONS.get(cat, "preferences-system")
            item.setIcon(QIcon.fromTheme(icon_name))
            if cat != "All Categories" and (cat not in self.services_data or not self.services_data[cat]):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setForeground(QColor("#666"))
            # Elide long names and add tooltip
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            item.setToolTip(cat)
            self.category_list.addItem(item)
            self.category_items.append(item)
        self.category_list.itemClicked.connect(self.on_category_selected)
        sidebar_layout.addWidget(self.category_list)
        sidebar.setLayout(sidebar_layout)
        content_layout.addWidget(sidebar)
        # Vertical separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        content_layout.addWidget(separator)
        # Services panel
        services_panel = QWidget()
        services_layout = QVBoxLayout()
        services_layout.setContentsMargins(0, 0, 0, 0)
        services_layout.setSpacing(4)
        services_panel.setStyleSheet('background: transparent; border: none;')
        services_header = QLabel("Services")
        services_header.setFont(QFont("San Francisco", 15, QFont.Weight.Bold))
        services_header.setStyleSheet('color: #fff; letter-spacing: 0.5px;')
        services_layout.addWidget(services_header)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search services...")
        self.search_bar.setClearButtonEnabled(True)
        services_layout.addWidget(self.search_bar)
        self.search_bar.textChanged.connect(self.on_search)
        self.services_list = QListWidget()
        self.services_list.setStyleSheet('QListWidget { background: transparent; border: none; font-size: 14px; } QListWidget::item { background: transparent; } QListWidget::item:alternate { background: #23282f; } QListWidget::item:selected { background: #007aff33; color: #fff; font-weight: 600; } QListWidget::item:hover { background: #2c2f36; }')
        self.services_list.setAlternatingRowColors(True)
        services_layout.addWidget(self.services_list)
        self.services_list.itemClicked.connect(self.on_service_selected)
        self.services_list.itemDoubleClicked.connect(self.on_service_toggle)
        self.services_placeholder = QLabel('No services in this category.')
        self.services_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.services_placeholder.setStyleSheet('color: #888; font-size: 13px;')
        self.services_placeholder.hide()
        services_layout.addWidget(self.services_placeholder)
        # Legend at the bottom
        legend = QLabel('🟢 Running   🟡 Enabled   🔴 Disabled   🟠 Pending')
        legend.setStyleSheet('font-size: 12px; color: #aaa; margin-top: 4px;')
        services_layout.addWidget(legend)
        services_panel.setLayout(services_layout)
        content_layout.addWidget(services_panel)
        # Details panel
        details_panel = QWidget()
        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(4)
        details_panel.setStyleSheet('background: transparent; border: none;')
        details_header = QLabel('Details')
        details_header.setFont(QFont("San Francisco", 15, QFont.Weight.Bold))
        details_header.setStyleSheet('color: #fff; letter-spacing: 0.5px;')
        details_layout.addWidget(details_header)
        self.details_box = QTextEdit()
        self.details_box.setReadOnly(True)
        self.details_box.setStyleSheet('background: transparent; border: none; color: #eaeaea; padding: 10px; font-size: 14px;')
        self.details_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        details_layout.addWidget(self.details_box)
        self.details_placeholder = QLabel('Select a service to see details.')
        self.details_placeholder.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.details_placeholder.setStyleSheet('color: #888; font-size: 13px;')
        details_layout.addWidget(self.details_placeholder)
        details_panel.setLayout(details_layout)
        content_layout.addWidget(details_panel)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        # Status area at the bottom, flush with edges
        self.status_label = QLabel('Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setStyleSheet('color: #eaeaea; font-size: 13px; padding: 4px 8px; background: #181a1b; border-radius: 0px; margin: 0px;')
        main_layout.addWidget(self.status_label)
        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)
            self.on_category_selected(self.category_list.item(0))
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_services)
        self.refresh_timer.start(5000)
        
    def populate_categories(self):
        """Populate the category list."""
        self.category_list.clear()
        for category in self.categories:
            item = QListWidgetItem(category)
            # Add icon if available
            if "Advertising" in category:
                item.setIcon(QIcon(":/icons/ads.png"))
            elif "App & Store" in category:
                item.setIcon(QIcon(":/icons/store.png"))
            elif "Hardware" in category:
                item.setIcon(QIcon(":/icons/hardware.png"))
            elif "Siri" in category:
                item.setIcon(QIcon(":/icons/siri.png"))
            else:
                item.setIcon(QIcon(":/icons/other.png"))
            self.category_list.addItem(item)
            
    def on_category_selected(self, item):
        """Handle category selection."""
        self.current_category = item.text()
        self.populate_services()
        self.details_box.clear()
        self.details_placeholder.setText('Select a service to see details.')
        self.details_placeholder.show()
        
    def populate_services(self):
        """Populate the service list for the selected category."""
        self.services_list.clear()
        if not self.current_category:
            return
        if self.current_category == "All Categories":
            # Show all services from all categories
            all_services = {}
            for cat, services in self.services_data.items():
                all_services.update(services)
            services = all_services
        elif self.current_category not in self.services_data:
            return
        else:
            services = self.services_data[self.current_category]
        # Sort services by status: running (0), enabled (1), disabled (2), then by name
        def status_sort_key(item):
            name, info = item
            # Use the original status for sorting, not pending_status
            status = info["status"]
            if status == "running":
                return (0, name)
            elif status == "enabled":
                return (1, name)
            else:
                return (2, name)
        sorted_services = sorted(services.items(), key=status_sort_key)
        for service_name, service_info in sorted_services:
            # If there is a pending change, show it visually but do not affect sorting
            if service_name in self.pending_changes:
                pending_status = self.pending_changes[service_name]
                service_info = dict(service_info)  # Copy to avoid mutating original
                service_info["pending_status"] = pending_status
            item = QListWidgetItem()
            # Create status indicator
            status = service_info.get("pending_status", service_info["status"])
            if "pending_status" in service_info and service_info["pending_status"] != service_info["status"]:
                status_icon = "🔄"
                color = QColor("#ff9500")  # Orange for pending
            elif status == "running":
                status_icon = "●"
                color = QColor("#34c759")  # Green
            elif status == "enabled":
                status_icon = "●"
                color = QColor("#ffcc00")  # Yellow
            elif status == "disabled":
                status_icon = "●"
                color = QColor("#ff3b30")  # Red
            else:
                status_icon = "●"
                color = QColor("#ff9500")  # Orange
            # Try to get CPU and RAM usage if running
            cpu_mem_str = ""
            pid = service_info.get("pid")
            if status == "running" and pid:
                try:
                    proc = psutil.Process(int(pid))
                    cpu = proc.cpu_percent(interval=0.05)
                    mem = proc.memory_info().rss // (1024 * 1024)
                    cpu_mem_str = f"  [CPU: {cpu:.1f}% | RAM: {mem}MB]"
                except Exception:
                    cpu_mem_str = ""
            item.setText(f"{status_icon}  {service_name}{cpu_mem_str}")
            item.setForeground(color)
            item.setData(Qt.ItemDataRole.UserRole, service_name)
            item.setToolTip(f"Status: {status.capitalize()}\nDouble-click to toggle.")
            self.services_list.addItem(item)
        self.services_placeholder.setVisible(self.services_list.count() == 0)
        
    def on_service_selected(self, item):
        """Handle service selection to show details."""
        service_name = item.data(Qt.ItemDataRole.UserRole)
        if not service_name or not self.current_category:
            return
        # Find the service info in the correct category if 'All Categories' is selected
        if self.current_category == "All Categories":
            # Search all categories for the service
            for cat_services in self.services_data.values():
                if service_name in cat_services:
                    service_info = cat_services[service_name]
                    break
            else:
                return
        else:
            service_info = self.services_data[self.current_category][service_name]
        self.show_service_details(service_name, service_info)
        self.details_placeholder.hide()
        
    def show_service_details(self, service_name, service_info):
        """Display service details in the details panel."""
        status = service_info.get("pending_status", service_info["status"])
        live_status = service_info["status"]
        details_html = f"""
        <div style='text-align:left;'>
        <div style='font-size:15px; font-weight:600; margin-bottom:6px;'>{service_name}</div>
        <div style='margin-bottom:4px;'><b>Type:</b> {service_info['type'].capitalize()}</div>
        <div style='margin-bottom:4px;'><b>Status:</b> {live_status.capitalize()}</div>
        """
        # Show pending changes
        if "pending_status" in service_info and service_info["pending_status"] != live_status:
            pending_status = service_info["pending_status"]
            details_html += f"<div style='margin-bottom:4px;'><b>Pending:</b> {pending_status.capitalize()} (double-click to toggle, click Apply to confirm)</div>"
        details_html += f"""
        <div style='margin-bottom:4px;'><b>Description:</b></div>
        <div style='margin-bottom:8px;'>{service_info['description']}</div>
        <div style='margin-bottom:4px;'><b>Impact of Disabling:</b></div>
        <div>{service_info['impact']}</div>
        </div>
        """
        self.details_box.setHtml(details_html)
        
    def on_service_toggle(self, item):
        """Toggle service enable/disable status."""
        service_name = item.data(Qt.ItemDataRole.UserRole)
        if not service_name or not self.current_category:
            return
        # Find the service info in the correct category if 'All Categories' is selected
        if self.current_category == "All Categories":
            for cat_services in self.services_data.values():
                if service_name in cat_services:
                    service_info = cat_services[service_name]
                    break
            else:
                return
        else:
            service_info = self.services_data[self.current_category][service_name]
        current_status = self.pending_changes.get(service_name, service_info["status"])
        # Toggle status
        new_status = "enabled" if current_status == "disabled" else "disabled"
        self.pending_changes[service_name] = new_status
        self.apply_btn.setEnabled(True)
        # Update display
        self.populate_services()
        self.show_service_details(service_name, dict(service_info, pending_status=new_status))
        
    def apply_changes(self):
        """Apply pending changes to services."""
        print("[DEBUG] apply_changes called")
        if not self.pending_changes:
            print("[DEBUG] No pending changes.")
            return
        self.set_status('Applying changes...')
        # Show confirmation dialog
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Changes")
        msg.setText(f"Apply changes to {len(self.pending_changes)} service(s)?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()
        print(f"[DEBUG] Confirmation dialog result: {result}")
        if result == QMessageBox.StandardButton.Yes:
            print("[DEBUG] User confirmed changes. Applying...")
            from core.service_manager import bootout_and_disable, bootout_and_disable_system_daemon, get_uid
            import subprocess
            import sys
            warnings = []
            uid = get_uid()
            for service_name, new_status in list(self.pending_changes.items()):
                # Find the service info in the correct category if 'All Categories' is selected
                if self.current_category == "All Categories":
                    for cat_services in self.services_data.values():
                        if service_name in cat_services:
                            service_info = cat_services[service_name]
                            break
                    else:
                        continue
                elif self.current_category and service_name in self.services_data[self.current_category]:
                    service_info = self.services_data[self.current_category][service_name]
                else:
                    continue
                if new_status == "disabled":
                    if service_info["type"] == "daemon":
                        QApplication.beep()
                        confirm_msg = QMessageBox()
                        confirm_msg.setIcon(QMessageBox.Icon.Warning)
                        confirm_msg.setWindowTitle("Confirm System Daemon Change")
                        confirm_msg.setText(f"You are about to stop and disable the system daemon '{service_name}'. This requires sudo and may impact system stability.\n\nAre you sure you want to proceed?")
                        confirm_msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                        confirm_result = confirm_msg.exec()
                        print(f"[DEBUG] Daemon confirm dialog result: {confirm_result}")
                        if confirm_result != QMessageBox.StandardButton.Yes:
                            print(f"[DEBUG] User cancelled daemon change for {service_name}")
                            continue  # Skip this daemon if not confirmed
                        self.set_status(f'Disabling system daemon: {service_name}...')
                        success, error = bootout_and_disable_system_daemon(service_name)
                        print(f"[DEBUG] bootout_and_disable_system_daemon({service_name}) -> {success}, {error}")
                        if not success:
                            warnings.append(f"[Daemon] {service_name}: {error}")
                    else:
                        self.set_status(f'Disabling agent: {service_name}...')
                        success, error = bootout_and_disable(service_name, uid)
                        print(f"[DEBUG] bootout_and_disable({service_name}, {uid}) -> {success}, {error}")
                        if not success:
                            warnings.append(f"[Agent] {service_name}: {error}")
                else:
                    if service_info["type"] == "daemon":
                        command = ["sudo", "launchctl", "enable", f"system/{service_name}"]
                    else:
                        command = ["launchctl", "enable", f"gui/{uid}/{service_name}"]
                    print(f"[DEBUG] Running command: {' '.join(command)}")
                    self.set_status(f'Enabling {service_info["type"]}: {service_name}...')
                    subprocess.run(command, capture_output=True, text=True, check=False)
                service_info["status"] = new_status
                if "pending_status" in service_info:
                    del service_info["pending_status"]
                # Remove from pending_changes after applying
                del self.pending_changes[service_name]
            if warnings:
                warning_text = "\n".join(warnings)
                QMessageBox.warning(self, "Warnings", f"Some services may not have been fully disabled:\n\n{warning_text}")
                self.set_status('Some services may not have been fully disabled.')
            else:
                QMessageBox.information(self, "Success", "Changes applied successfully!")
                self.set_status('Changes applied successfully!')
            self.apply_btn.setEnabled(False)
            self.populate_services()
            self.details_box.clear()
            self.details_placeholder.setText('Select a service to see details.')
            self.details_placeholder.show()
            self.set_status('Ready')
        
    def go_back(self):
        """Return to welcome screen."""
        # This will be handled by the main window
        pass 

    def on_search(self, text):
        """Filter services by search query (name or description)."""
        query = text.strip().lower()
        # Only filter the currently visible list, do not re-query backend
        if not self.current_category:
            return
        if self.current_category == "All Categories":
            all_services = {}
            for cat, services in self.services_data.items():
                all_services.update(services)
            services = all_services
        elif self.current_category not in self.services_data:
            self.services_list.clear()
            self.services_placeholder.show()
            return
        else:
            services = self.services_data[self.current_category]
        matches = []
        for name, info in services.items():
            if query in name.lower() or query in info.get('description', '').lower():
                matches.append((name, info))
        self.services_list.clear()
        if not matches:
            self.services_placeholder.setText('No services match your search.')
            self.services_placeholder.show()
        else:
            self.services_placeholder.hide()
            # Use the same sorting as populate_services
            def status_sort_key(item):
                name, info = item
                status = info["status"]
                if status == "running":
                    return (0, name)
                elif status == "enabled":
                    return (1, name)
                else:
                    return (2, name)
            sorted_matches = sorted(matches, key=status_sort_key)
            for service_name, service_info in sorted_matches:
                if service_name in self.pending_changes:
                    pending_status = self.pending_changes[service_name]
                    service_info = dict(service_info)
                    service_info["pending_status"] = pending_status
                item = QListWidgetItem()
                status = service_info.get("pending_status", service_info["status"])
                if "pending_status" in service_info and service_info["pending_status"] != service_info["status"]:
                    status_icon = "🔄"
                    color = QColor("#ff9500")
                elif status == "running":
                    status_icon = "●"
                    color = QColor("#34c759")
                elif status == "enabled":
                    status_icon = "●"
                    color = QColor("#ffcc00")
                elif status == "disabled":
                    status_icon = "●"
                    color = QColor("#ff3b30")
                else:
                    status_icon = "●"
                    color = QColor("#ff9500")
                item.setText(f"{status_icon}  {service_name}")
                item.setForeground(color)
                item.setData(Qt.ItemDataRole.UserRole, service_name)
                item.setToolTip(f"Status: {status.capitalize()}\nDouble-click to toggle.")
                self.services_list.addItem(item)

    def apply_theme(self):
        # Remove per-widget theme application; rely on main window
        pass
    def apply_dark_theme(self):
        pass
    def apply_light_theme(self):
        pass 

    def refresh_services(self):
        self.set_status('Refreshing services...')
        from core.service_manager import get_live_services
        self.services_data = get_live_services()
        # Reapply pending changes to the refreshed data
        for service_name, pending_status in self.pending_changes.items():
            # Find the service in any category
            for cat_services in self.services_data.values():
                if service_name in cat_services:
                    cat_services[service_name]["pending_status"] = pending_status
        self.populate_services()
        self.set_status('Ready')

    def set_status(self, message):
        self.status_label.setText(message) 