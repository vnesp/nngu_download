import requests
from bs4 import BeautifulSoup

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

page = requests.get(url, params)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table', {'id': 'jtable'})
for row in table.tbody.findChildren('tr', recursive=False):
    cells = row.findChildren('td', recursive=False)
    if cells[1].has_attr('colspan'):
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