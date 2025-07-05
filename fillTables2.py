import api
import bs4
import re
import db

def proceed(facId, specId, finId, formId):
    print(f'GET fac {facId}, spec {specId}, fin {finId}, form {formId}')
    table = bs4.BeautifulSoup(
        api.show(1, 1, spec=specId, fac=facId, fin=finId, form=formId),
        'html.parser'
    ).find('table', {'id': 'jtable'})
    specVarId = specId[15:]
    for row in table.tbody.findChildren('tr', recursive=False):
        cells = row.findChildren('td', recursive=False)
        res = re.fullmatch('\d+\. (.*?)(\. Количество мест: (\d+))?', cells[0].text)
        assert res, cells[0].text
        if res.group(1) == 'Бюджет (общий конкурс)':
            print(f'NumPlaces = {res.group(3)}')
            db.insert('Direction', (None, facId, specVarId, finId, formId, res.group(3)))
            break
    else:
        db.insert('Direction', (None, facId, specVarId, finId, formId, 0))
    # with open('show.html', 'wb') as file:
    #     file.write(page)


facIds = db.select('Faculties', 'ID')

for facId, in facIds:

    def getSpecs():

        def getFins(specId):

            def getForms(finId):
                if finId == '-1':
                    return
                menu = bs4.BeautifulSoup(api.menu(1, 1, spec=specId, fac=facId, fin=finId), 'html.parser')
                select = menu.find('select', {'id': 'form'})
                for option in select.findChildren('option', recursive=False):
                    formId = option['value']
                    if formId == '-1':
                        continue
                    proceed(facId, specId, finId, formId)

            if specId == '-1':
                return
            menu = bs4.BeautifulSoup(api.menu(1, 1, spec=specId, fac=facId), 'html.parser')
            select = menu.find('select', {'id': 'fin'})
            for option in select.findChildren('option', recursive=False):
                getForms(option['value'])

        menu = bs4.BeautifulSoup(api.menu(1, 1, fac=facId), 'html.parser')
        select = menu.find('select', {'id': 'spec'})
        for option in select.findChildren('option', recursive=False):
            getFins(option['value'])

    getSpecs()

db.flush()
