# Телеграм-бот для игры в банальности

* `create_base.sql` - sql-скрипт для создания базы
* `main.py` - основной скрипт

Установка BeautifulSoup

``` bash
pip install beautifulsoup4
```

Создание базы

``` bash
sqlite3 base.db < create_base.sql
```

Запуск

``` bash
python main.py
```
