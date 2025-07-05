# Сборщик и парсер данных по поступлению

* `create_base.sql` - sql-скрипт для создания базы
* `main.py` - основной скрипт (Work In Progress)
* `db.py` - библиотека для работы с базой
* `api.py` - API для запросов к сайту
* `fillTables.py` - скрипт для заполнения таблиц факультетов, специальностей, финансирования и форм обучения

Установка BeautifulSoup

``` bash
pip install beautifulsoup4
```

Создание базы

``` bash
sqlite3 base.db < createBase.sql
```

Заполнение вспомогательных таблиц

``` bash
python fillTables.py
```

Запуск

``` bash
python main.py
```
