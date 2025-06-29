import requests

BASE_URL = 'https://abiturient.unn.ru/list'

session = requests.session()

def get(cmd, params = None):
    response = session.get(f'{BASE_URL}/{cmd}.php', params=params)
    response.raise_for_status()
    return response.content

def index(list, level):
    """ Get Index
      :param list: Тип списка
       = 1 - Динамические списки
       = 2 - Конкурсные списки
       = 3 - Список подавших документы

      :param level: Уровень образования
       = 1 - Бакалавриат и специалитет
       = 2 - Магистратура
       = 3 - Среднее профессиональное
       = 4 - Ординатура
       = 5 - Аспирантура
    """
    return get('index', {
        'list': list,
        'level': level,
    })

def menu(list, level, spec=-1, fac=-1, fin=-1, form=-1, dop=0):
    return get('menu', {
        'list': list,
        'level': level,
        'spec': spec,
        'fac': fac,
        'fin': fin,
        'form': form,
        'dop': dop,
    })
