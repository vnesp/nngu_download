import api
import bs4
import re
import db

abit = {}
dir = []
status = {}
quotes = {}


def getClass(soup):
    for cls in soup['class']:
        if cls.startswith('fa-'):
            return cls[3:]


def proceed(facId, specId, finId, formId):
    print('      GET fac {}, spec {}, fin {}, form {}'.format(facId, specId, finId, formId))
    page = api.show(1, 1, spec=specId, fac=facId, fin=finId, form=formId)
    with open('show.html', 'w', encoding='utf8') as file:
        file.write(page)
    table = bs4.BeautifulSoup(page,'html5lib').find('table', {'id': 'jtable'})
    specVarId = specId[15:]
    countItems = 0
    dirIdForList = {}
    for row in table.tbody.findChildren('tr', recursive=False):
        cells = row.findChildren('td', recursive=False)
        assert len(cells) == 12, cells
        res = re.fullmatch('(\d+)\. (.*?)(\. Количество мест: (\d+))?', cells[0].text)
        assert res, cells[0].text
        listCount, quoteName, numPlaces = res.group(1, 2, 4)
        quoteId = quotes.get(quoteName, len(quotes))
        quotes[quoteName] = quoteId
        dirValue = (facId, specVarId, finId, formId, quoteId, numPlaces)
        if listCount in dirIdForList:
            dirId = dirIdForList[listCount]
            assert dir[dirId] == dirValue, (dir[dirId], dirValue)
        else:
            dirId = len(dir)
            dirIdForList[listCount] = dirId
            print('      New direction', dirValue)
            dir.append(dirValue)
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
        countItems += 1

    print('      Abiturients:', countItems, 'added')


def getForms(facId, specId, finId):
    if finId == '-1':
        return
    print('    Get Forms from fin =', finId)
    menu = bs4.BeautifulSoup(api.menu(1, 1, spec=specId, fac=facId, fin=finId), 'html5lib')
    select = menu.find('select', {'id': 'form'})
    for option in select.findChildren('option', recursive=False):
        formId = option['value']
        if formId == '-1':
            continue
        proceed(facId, specId, finId, formId)


def getFins(facId, specId):
    if specId == '-1':
        return
    print('  Get Fins from spec =', specId)
    menu = bs4.BeautifulSoup(api.menu(1, 1, spec=specId, fac=facId), 'html5lib')
    select = menu.find('select', {'id': 'fin'})
    for option in select.findChildren('option', recursive=False):
        getForms(facId, specId, option['value'])


def getSpecs(facId):
    print('Get spec from fac =', facId)
    menu = bs4.BeautifulSoup(api.menu(1, 1, fac=facId), 'html5lib')
    select = menu.find('select', {'id': 'spec'})
    for option in select.findChildren('option', recursive=False):
        getFins(facId, option['value'])

facIds = db.select('Faculties', 'ID')
print('Faculties =', facIds); 
for facId, in facIds:
    getSpecs(facId)
db.flush()

db.insertmany('Abiturients', 2, abit.items())
db.flush()

db.insertmany('Directions', 7, ((id, *value) for id, value in enumerate(dir)))
db.flush()

db.insertmany('Statuses', 2, ((id, text) for text, id in status.items()))
db.flush()

db.insertmany('Quotes', 2, ((id, text) for text, id in quotes.items()))
db.flush()
