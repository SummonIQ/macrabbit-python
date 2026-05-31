from setuptools import setup

APP = ['main_gui.py']
DATA_FILES = [('', ['theme.qss'])]
OPTIONS = {
    'argv_emulation': True,
    'includes': [
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtCore',
        'core',
    ],
    'iconfile': 'app_icon.png',
    'plist': {
        'CFBundleName': 'macOS Service Manager',
        'CFBundleDisplayName': 'macOS Service Manager',
        'CFBundleIdentifier': 'com.macosservice.manager',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSMinimumSystemVersion': '10.14',
        'NSAppleEventsUsageDescription': 'This app manages system services.'
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 