# coding:utf-8
import json
import os

# глобальные переменные
file_path_from = 'C:\TEMP\DEDUP_JSON\FROM\\' # Путь к корневому каталогу хранения исходных JSON файлов
file_path_to = 'C:\TEMP\DEDUP_JSON\TO\\' # Путь к корневому каталогу хранения результирующих JSON файлов
dictionary = {'liabilityDedupIntIndividual', 'liabilityDedupIntLegalEntity'}  # словарь с названием очищаемых массивов


# Очищаем массив с результатами дедубликации
def clean_arr(d):
    if not isinstance(d, (dict, list)): return d
    elif isinstance(d, list): return [v for v in (clean_arr(v) for v in d)]
    else:
        for k, v in d.items():
            if k in dictionary:
                d[k] = []
        return {k: v for k, v in ((k, clean_arr(v)) for k, v in d.items())}


# По всем файлам JSON папке file_path_from
for entry in os.scandir(file_path_from):
    if entry.is_file() and entry.name.endswith('.json'):
        # Загружаем файл JSON
        with open(file_path_from + entry.name, encoding='utf-8') as fh:
            to_json = clean_arr(json.load(fh))
        # Сохраняем обработанный файл JSON
        with open(file_path_to + entry.name, 'w', encoding='utf-8') as outfile:
            json.dump(to_json, outfile, indent=2, ensure_ascii=False)

