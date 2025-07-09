import api
import bs4
import re
import db

menu = bs4.BeautifulSoup(api.menu(1, 1), 'html5lib')

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
        print(res[1].groups())
        for item in saveto:
            db.insert(item['table'], tuple(res[i].group(j) for i, j in item['record']))

db.flush()