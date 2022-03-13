# Установка сборщика

1. pip install pypiwin32
1. pip install pyinstaller
1. pyinstaller --version

# Сборка

1. pyinstaller --paths venv/Lib/site-packages --windowed word_generator.py --add-data "templates.txt;." --noconfirm
1. pyinstaller --paths venv/Lib/site-packages --windowed eda_generator.py --add-data "templates.txt;." --noconfirm

