import api
import bs4
import re
import db

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
                    page = api.show(1, 1, spec=specId, fac=facId, fin=finId, form=formId)
                    with open('show.html', 'wb') as file:
                        file.write(page)
                    exit()

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
    break

exit()

menu = bs4.BeautifulSoup(api.menu(1, 1), 'html.parser')

structure = {
    'form': {
        'regexp': (r'(\d)', r'(.*)'),
        'saveto': [{
            'table': 'FormEducations',
            'record': ((0,1), (1,1))
        }]
    },
    'fac': {
        'regexp': (r'(\d{15})', r'(.*)'),
        'saveto': [{
            'table': 'Faculties',
            'record': ((0,1), (1,1))
        }]
    },
    'fin': {
        'regexp': (r'(\d{15})', r'(.*)'),
        'saveto': [{
            'table': 'FundingSources',
            'record': ((0,1), (1,1))
        }]
    },
    'spec': {
        'regexp': (r'(\d{15})(\d{15})', r'(.*?) \((\d{2}\.\d{2}\.\d{2})\)  / (.*)'),
        'saveto': [{
            'table': 'Specializations',
            'record': ((0,1), (1,2), (1,1))
        },{
            'table': 'SpecializationVariants',
            'record': ((0,2), (0,1), (1,3))
        }]
    }
}

for select in menu.findChildren('select'):
    obj = structure.get(select['name'])
    if obj is None:
        continue
    regexp = obj['regexp']
    saveto = obj['saveto']
    for option in select.findChildren('option'):
        _id = option['value']
        if _id == '-1':
            continue
        res = (
            re.fullmatch(regexp[0], _id),
            re.fullmatch(regexp[1], option.text)
        )
        assert all(res)
        for item in saveto:
            db.insert(item['table'], tuple(res[i].group(j) for i, j in item['record']))
