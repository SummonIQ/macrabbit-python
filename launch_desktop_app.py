#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def main():
    desktop = Path.home() / 'Desktop'
    app_alias = desktop / 'macOS Service Manager'
    if app_alias.exists():
        print('Launching macOS Service Manager from Desktop shortcut...')
        subprocess.run(['open', str(app_alias)])
    else:
        print('Desktop shortcut not found!')
        print('Please run create_desktop_shortcut.py first, or launch the app from dist/macOS Service Manager.app')

if __name__ == '__main__':
    main() 