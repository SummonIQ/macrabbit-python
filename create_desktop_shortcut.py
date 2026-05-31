#!/usr/bin/env python3
"""
Create a desktop shortcut to the macOS Service Manager app.
This creates an alias on the desktop that can be double-clicked to launch the app.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_desktop_shortcut():
    """Create a desktop shortcut to the app bundle."""
    
    # Get the current directory (where the app bundle is)
    current_dir = Path.cwd()
    app_bundle_path = current_dir / "dist" / "macOS Service Manager.app"
    
    # Get the desktop path
    desktop_path = Path.home() / "Desktop"
    
    # Create the shortcut name
    shortcut_name = "macOS Service Manager"
    shortcut_path = desktop_path / shortcut_name
    
    # Check if app bundle exists
    if not app_bundle_path.exists():
        print(f"Error: App bundle not found at {app_bundle_path}")
        print("Please build the app first with: python3 setup.py py2app")
        return False
    
    try:
        # Create an alias using macOS's built-in alias creation
        cmd = [
            "osascript", "-e",
            f'tell application "Finder" to make alias file to POSIX file "{app_bundle_path}" at POSIX file "{desktop_path}"'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Desktop shortcut created successfully!")
            print(f"   Location: {desktop_path / 'macOS Service Manager'}")
            print(f"   You can now double-click the shortcut on your desktop to launch the app.")
            return True
        else:
            print(f"Error creating shortcut: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("Creating desktop shortcut for macOS Service Manager...")
    
    if create_desktop_shortcut():
        print("\n🎉 Success! You now have a desktop shortcut to launch the app.")
        print("   Just double-click the 'macOS Service Manager' icon on your desktop.")
    else:
        print("\n❌ Failed to create desktop shortcut.")
        print("   You can still launch the app by double-clicking 'launch_app.command'")

if __name__ == "__main__":
    main() 