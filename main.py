# coding:utf-8
import json
import os

# глобальные переменные
file_name_edto = 'edto.json'  # Файл eDTO, из которого переносим описание полей
file_name_swagger = 'swagger.json'  # Файл swagger, в который добавляем описание


# Заполняем словарь с описание полей
def change_def(d, targetkey, parenttargetkey, blokName):
    if not isinstance(d, (dict, list)):
        if targetkey == 'description':
            return d
        return d
    elif isinstance(d, list):
        return [v for v in (change_def(v, targetkey, parenttargetkey, blokName) for v in d)]
    else:
        return {k: v for k, v in ((k, change_def(v, k, targetkey,  blokName)) for k, v in d.items())}


# Загружаем файл eDTO
with open(file_name_edto, encoding='utf-8') as fh:
    modelDefinitions = json.load(fh)['definitions']

# Перебираем все eDTO и считываем описание для полей с привязкой к ДТО
for key in modelDefinitions:
    change_def(modelDefinitions[key], key, key, key)

