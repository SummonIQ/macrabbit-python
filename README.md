<!-- SUMMONIQ-OSS-HEADER:START -->
<div align="center">

  <img src="app_icon.png" alt="Mac Rabbit logo" width="112">

  <h1>Mac Rabbit</h1>
  <p>A native macOS application for managing system services and optimizing your Mac's performance and privacy.</p>

  <p>
    <a href="https://github.com/SummonIQ/mac-rabbit"><img alt="Repository" src="https://img.shields.io/badge/github-SummonIQ%2Fmac-rabbit-24292f?logo=github"></a>
    <a href="https://unlicense.org/"><img alt="License: Unlicense" src="https://img.shields.io/badge/license-Unlicense-blue.svg"></a>
  </p>

</div>

---
<!-- SUMMONIQ-OSS-HEADER:END -->
# macOS Service Manager

A native macOS application for managing system services and optimizing your Mac's performance and privacy.

## 🚀 Quick Start

### Option 1: Desktop Shortcut (Recommended)
- Double-click the **"macOS Service Manager"** icon on your desktop
- The app will launch with a beautiful native macOS interface

### Option 2: Command Line Launcher
- Double-click `launch_app.command` in this folder
- This will launch the app and show status messages

### Option 3: Direct App Bundle
- Navigate to `dist/macOS Service Manager.app`
- Double-click the app bundle

## ✨ Features

### 🎯 Quick Optimization
- **Touch Bar Disable**: Disables Touch Bar services for better performance
- **Siri Disable**: Turns off Siri and related services for privacy
- **Spotlight Disable**: Disables Spotlight indexing and services
- **UI Enhancements**: Disables animations, transparency, and dock effects
- **Dock Optimizations**: Reduces dock animations and effects
- **Analytics Disable**: Stops Apple's analytics and telemetry services

### 🔧 Service Management
- **Browse by Category**: Services organized into logical categories
- **Real-time Status**: See which services are running, disabled, or stopped
- **Detailed Information**: View descriptions and impact of each service
- **One-click Control**: Enable/disable services with a single click
- **System & User Services**: Manage both system daemons and user agents

## 🛡️ Safety Features

- **Verification**: App verifies that services are actually disabled
- **Warnings**: Shows warnings for services that can't be disabled
- **Backup**: Services can be re-enabled if needed
- **Non-destructive**: Only disables services, doesn't delete them

## 📋 Requirements

- macOS 10.14 (Mojave) or later
- Administrator privileges (for system service management)
- No additional software required (self-contained app)

## 🔧 Building from Source

If you want to rebuild the app:

```bash
# Install dependencies
pip install PyQt6 py2app pillow

# Build the app bundle
python3 setup.py py2app

# Create desktop shortcut
python3 create_desktop_shortcut.py
```

## 🎨 Design

This app follows Apple's Human Interface Guidelines:
- Native macOS look and feel
- System fonts and colors
- Proper spacing and typography
- Accessibility support
- High-resolution display support

## 📱 Usage Tips

1. **Start with Quick Optimization**: Use the "Quick Optimization" feature first for common improvements
2. **Review Before Applying**: Check the service details before disabling
3. **Monitor Performance**: Notice improved battery life and reduced background activity
4. **Re-enable if Needed**: Services can be re-enabled if you encounter issues

## 🔍 Troubleshooting

- **App won't launch**: Make sure you have administrator privileges
- **Services still running**: Some services may restart automatically; use the verification feature
- **Permission errors**: The app needs administrator access to manage system services

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: This app modifies system services. While it's designed to be safe, always review what you're disabling and keep backups of important data.
