#!/bin/zsh

# macOS Service Manager Launcher
# Double-click this file to launch the app

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the app bundle
APP_PATH="$SCRIPT_DIR/dist/macOS Service Manager.app"

# Check if the app bundle exists
if [ ! -d "$APP_PATH" ]; then
    echo "Error: App bundle not found at $APP_PATH"
    echo "Please make sure the app has been built with: python3 setup.py py2app"
    read -p "Press Enter to exit..."
    exit 1
fi

# Launch the app
echo "Launching macOS Service Manager..."
open "$APP_PATH"

# Optional: Wait a moment and check if the app launched successfully
sleep 2
if pgrep -f "macOS Service Manager" > /dev/null; then
    echo "App launched successfully!"
else
    echo "App may have failed to launch. Check the Console app for errors."
fi 