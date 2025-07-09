import requests
import sqlite3
from bs4 import BeautifulSoup

dbConn = sqlite3.connect('base.db')
dbCursor = dbConn.cursor()

def getId(table, field, value):
    dbCursor.execute(f"""
        INSERT OR IGNORE INTO {table} ({field})
            VALUES (?)
    """, (value,))
    result = dbCursor.execute(f"""
        SELECT ID FROM {table}
            WHERE {field} = ?
    """, (value,)).fetchone()
    return result[0]

url = 'https://abiturient.unn.ru/list/show.php'

params = {
    'spec': '281474976710726281474976711093',
    'level': 1,
    'fac': '281474976710980',
    'dop': 0,
    'fin': '281474976719885',
    'form': 0,
    'list': 3
}

def getClass(soup):
    for cls in soup['class']:
        if cls.startswith('fa-'):
            return cls[3:]

def getPriorities(url, AbiturientID):
    print(url)
    page = requests.get('https://abiturient.unn.ru/list/' + url)
    # with open('abit.html', 'wb') as file:
    #     file.write(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', {'id': 'jtable'})
    for row in table.tbody.findChildren('tr', recursive=False):
        cells = row.findChildren('td', recursive=False)
        spec = cells[1].a.text.split(' / ')
        (
            AbiturientID,
            getId('Faculties', 'Name', cells[2].text),
            getId('Specializations', 'Name', spec[0]),
            getId('SpecializationVariants', 'Name', spec[1]), # Cod, Quantity - ???
            int(cells[5].text), # Prioritet
            cells[8].span.text.strip(), # Status
            int(cells[10].text.strip()), # NumSpis
            int(cells[9].text.strip()), # NumIfOrig
            getId('FormEducations', 'Name', cells[3].text), # FormEdID
            getId('FundingSources', 'Name', cells[4].text)  # FunSourceID
        )

page = requests.get(url, params)
soup = BeautifulSoup(page.content.decode('utf8'), 'html5lib')
table = soup.find('table', {'id': 'jtable'})
for row in table.tbody.findChildren('tr', recursive=False):
    cells = row.findChildren('td', recursive=False)
    if 'displaynone' in cells[1].get('class', []) or cells[1].has_attr('colspan'):
        continue
    # for idx, cell in enumerate(cells):
    #     print(idx, cell)
    obj = {
        'direction': cells[0].string,
        'order': int(cells[1].string),
        'code': int(cells[2].a.string),
        'url': cells[2].a['href'],
        'agreement': getClass(cells[3].i),
        'total': int(cells[4].string),
        'sum_withoud_id': int(cells[5].string),
        'priority': int(cells[6].string.strip()),
        'disciplines': [cells[i].string for i in range(7, 11)],
        'objective_id': cells[11].string,
        'info': cells[12].string,
        'olympiad_rank': cells[13].string,
        'high_priority': getClass(cells[14].i),
        'prior_rights': [getClass(cells[i].i) for i in range(15, 18)],
        'type': cells[18].string,
        'status': cells[19].span.string
    }
    print(obj)
    break
    AbuturientID = getId('Abiturients', 'Cod', obj['code'])
    getPriorities(obj['url'], AbuturientID)
