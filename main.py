# coding:utf-8
import json
import os
import csv

# глобальные переменные
file_path_from = 'C:\TEMP\PIM_JSON\FROM\\' # Путь к корневому каталогу хранения исходных JSON файлов
file_path_to = 'C:\TEMP\PIM_JSON\TO\eDtoFields.csv' # Путь к результирующим файлам

# словарь параметров заявки
dictionaryApp = {'loanApplication':['okpd','contractSum','contractPeriod'], 'beneficiary':['taxPayerNum'], 'creditParameters': ['creditTime','requestedSum']}
# словарь параметров заемщика
ROLE = 'borrower'
dictionaryLegal = {ROLE:['activityKindMdmId','customerMdmId','tin','businessRegDate']}
# словарь параметров модели
dictionaryModel = {'modelParameters': ['cnt_term_12','active_time','sum_any_12','cnt_any_12']}
resultList=[] # пустой лист для формирования строки
csvList=[] # пустой лист для формирования масива строк CSV

# Метод поиска и записи массива требуемых параметров
def getBorrowerParameters(d):
    if not isinstance(d, (dict, list)): return d
    elif isinstance(d, list): return [v for v in (getBorrowerParameters(v) for v in d)]
    else:
        for k, v in d.items():
            if k in dictionaryApp:
                for i in dictionaryApp[k]:
                    resultList.append(d[k][i])

            # Просматриваем роли и находим ЮЛ с нужной ролью
            if (k in {'roles'} and v!=None) and ROLE in v[0]:
                for i in dictionaryLegal[ROLE]:
                    resultList.append(d[i])

                for param in dictionaryModel['modelParameters']:
                    paramValue = ""
                    for x in d['modelResult']:
                        for y in x['modelParameters']:
                            if y['parameterName']==param:
                                paramValue = y['parameterValue']
                    resultList.append(paramValue)

        return {k: v for k, v in ((k, getBorrowerParameters(v)) for k, v in d.items())}


# По всем файлам JSON папке file_path_from
for entry in os.scandir(file_path_from):
    if entry.is_file() and entry.name.endswith('.json'):
        # Загружаем файл JSON
        with open(file_path_from + entry.name, encoding='utf-8') as fh:
            resultList = []
            to_json = getBorrowerParameters(json.load(fh))
            csvList.append(resultList)

# Формируем заголовки
header = []
for i, j in dictionaryApp.items():
    for t in j:
        header.append(t)

for i, j in dictionaryLegal.items():
    for t in j:
        header.append(t)

for i, j in dictionaryModel.items():
    for t in j:
        header.append(t)

# формируем CSV
with open(file_path_to, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(csvList)
