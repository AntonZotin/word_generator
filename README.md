# Установка сборщика

1. pip install pypiwin32
1. pip install pyinstaller
1. pyinstaller --version

# Сборка

1. pyinstaller --paths venv/Lib/site-packages --windowed word_generator.py --add-data "templates.txt;." --noconfirm


Вычисление ИНН

```python
inn = "7825058188"
response1 = requests.post("https://egrul.nalog.ru/", data={"query": inn}).json()
res1 = response1['t']
response2 = requests.get(f'https://egrul.nalog.ru/search-result/{res1}').json()
res2 = response2['rows'][0]['n']
```
