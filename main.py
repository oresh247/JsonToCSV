# coding:utf-8
import json
import os

# глобальные переменные
file_name_edto = 'edto.json'  # Файл eDTO, из которого переносим описание полей
file_name_swagger = 'swagger.json'  # Файл swagger, в который добавляем описание
file_name_swagger_new = 'swagger_new.json'  # Файл swagger, в который добавляем описание
dictionary = {}  # словарь с описанием полей

# Заполняем словарь с описание полей
def add_def_to_dict(d, targetkey, parenttargetkey, blokName):
    if not isinstance(d, (dict, list)):
        if targetkey == 'description': dictionary[blokName + '_' + parenttargetkey] = d
        return d
    elif isinstance(d, list): return [v for v in (add_def_to_dict(v, targetkey, parenttargetkey, blokName) for v in d)]
    else: return {k: v for k, v in ((k, add_def_to_dict(v, k, targetkey, blokName)) for k, v in d.items())}


# Дополняем описание из словаря
def change_def(v):
    for keydto in v['definitions']:
        for key in v['definitions'][keydto]['properties']:
            dickey = keydto + '_' + key
            if dickey in dictionary: v['definitions'][keydto]['properties'][key]['description'] = dictionary[dickey]
    return v


# Загружаем файл eDTO
with open(file_name_edto, encoding='utf-8') as fh:
    modelDefinitions = json.load(fh)['definitions']


# Перебираем все eDTO и считываем описание для полей с привязкой к ДТО
for key in modelDefinitions:
    add_def_to_dict(modelDefinitions[key], key, key, key)


# Загружаем файл swagger
with open(file_name_swagger, encoding='utf-8') as fd:
    swagger = json.load(fd)


# Перебираем все DTO в swagger и дополняем описание
swagger = change_def(swagger)


# Сохраняем новую модель SWAGGER в файл
with open(file_name_swagger_new, 'w', encoding='utf-8') as outfile:
    json.dump(swagger, outfile, indent=2, ensure_ascii=False)

