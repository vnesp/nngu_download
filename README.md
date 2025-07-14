# Сборщик и парсер данных по поступлению

* `create_base.sql` - sql-скрипт для создания базы
* `main.py` - основной скрипт (Work In Progress)
* `db.py` - библиотека для работы с базой
* `api.py` - API для запросов к сайту
* `fillTables.py` - скрипт для заполнения таблиц факультетов, специальностей, финансирования и форм обучения
* `fillTables2.py` - скрипт для заполнения таблицы направлений с количеством бюджетных мест, вид квот, статусов, абитуриентов и динамических списков

Установка BeautifulSoup, html5lib и requests

``` bash
pip install beautifulsoup4
pip install html5lib
pip install requests
```

Создание базы

``` bash
sqlite3 base.db < createBase.sql
```

Заполнение вспомогательных таблиц

``` bash
python fillTables.py
```

Заполнение количества бюджетных мест и динамических списков

``` bash
python fillTables2.py
```

Запуск (в процессе разработки)

``` bash
python main.py
```
