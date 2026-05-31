#!/bin/zsh
cd "$(dirname "$0")"
pip install -q PyQt6 psutil rich 2>/dev/null
python3 main_gui.py
