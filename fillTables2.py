import api
import bs4
import re
import db

abit = {}
dir = {}
status = {}

def getClass(soup):
    for cls in soup['class']:
        if cls.startswith('fa-'):
            return cls[3:]


def proceed(facId, specId, finId, formId):
    print(f'GET fac {facId}, spec {specId}, fin {finId}, form {formId}')
    page = api.show(1, 1, spec=specId, fac=facId, fin=finId, form=formId)
    with open('show.html', 'wb') as file:
        file.write(page)
    table = bs4.BeautifulSoup(page,'html.parser').find('table', {'id': 'jtable'})
    specVarId = specId[15:]
    dirKey = (facId, specVarId, finId, formId)
    dirId, NumPlaces = dir.get(dirKey, (len(dir), 0))
    for row in table.tbody.findChildren('tr', recursive=False):
        cells = row.findChildren('td', recursive=False)
        assert len(cells) == 12, cells
        if not NumPlaces:
            res = re.fullmatch('\d+\. (.*?)(\. Количество мест: (\d+))?', cells[0].text)
            assert res, cells[0].text
            if res.group(1) == 'Бюджет (общий конкурс)':
                NumPlaces = int(res.group(3))
        if 'displaynone' in cells[1].get('class', []) or cells[1].has_attr('colspan'):
            continue
        abitId = int(cells[2].a['href'].split('=')[1])
        abitCode = cells[2].a.text
        abit.setdefault(abitId, abitCode)
        assert abit[abitId] == abitCode
        statusText = cells[11].span.text.strip()
        if statusText != '':
            statusId = status.get(statusText, len(status))
            status[statusText] = statusId
        else:
            statusId = None

        db.insert('DynamicLists', (
            None,                               # ID
            dirId,                              # DirectionID
            int(cells[1].text),                 # NumGeneral
            abitId,                             # AbiturientID
            getClass(cells[3].i) == 'check',    # Consent
            int(cells[6].text.strip()),         # NumPrioritet
            cells[7].text,                      # Mark1
            cells[8].text,                      # Mark2
            cells[9].text,                      # Mark3
            cells[10].text,                     # MarkAchievemnt
            statusId                            # StatusID
        ))

    if NumPlaces:
        print(f'NumPlaces = {NumPlaces}')
    dir[dirKey] = (dirId, NumPlaces)

def getForms(facId, specId, finId):
    if finId == '-1':
        return
    menu = bs4.BeautifulSoup(api.menu(1, 1, spec=specId, fac=facId, fin=finId), 'html.parser')
    select = menu.find('select', {'id': 'form'})
    for option in select.findChildren('option', recursive=False):
        formId = option['value']
        if formId == '-1':
            continue
        proceed(facId, specId, finId, formId)


def getFins(facId, specId):
    if specId == '-1':
        return
    menu = bs4.BeautifulSoup(api.menu(1, 1, spec=specId, fac=facId), 'html.parser')
    select = menu.find('select', {'id': 'fin'})
    for option in select.findChildren('option', recursive=False):
        getForms(facId, specId, option['value'])


def getSpecs(facId):
    menu = bs4.BeautifulSoup(api.menu(1, 1, fac=facId), 'html.parser')
    select = menu.find('select', {'id': 'spec'})
    for option in select.findChildren('option', recursive=False):
        getFins(facId, option['value'])


for facId, in db.select('Faculties', 'ID'):
    getSpecs(facId)
db.flush()

db.insertmany('Abiturients', 2, abit.items())
db.flush()

db.insertmany('Directions', 6, ((id, *key, num) for key, (id, num) in dir.items()))
db.flush()

db.insertmany('Statuses', 2, ((id, text) for text, id in status.items()))
db.flush()
