# Установка сборщика

1. pip install pypiwin32
1. pip install pyinstaller
1. pyinstaller --version

# Сборка

1. pyinstaller --hidden-import python-docx, --hiddenimport PySimpleGUI, --hiddenimport openpyxl --windowed --onefile app.py
