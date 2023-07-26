# coding:utf-8
import json
import os
import csv

# глобальные переменные
file_path_from = 'C:\TEMP\PIM_JSON\FROM\\' # Путь к корневому каталогу хранения исходных JSON файлов
file_path_to = 'C:\TEMP\PIM_JSON\TO\eDtoFields.csv' # Путь к результирующим файлам

# словарь параметров заявки
dictionaryApp = {'loanApplication':['okpd', 'contractSum', 'contractPeriod'], 'beneficiary': ['taxPayerNum'], 'creditParameters': ['creditTime', 'requestedSum']}
#dictionaryApp = {'loanApplication':['okpd']}

# словарь параметров заемщика
ROLE = 'borrower'
MODEL = '1825'
dictionaryLegal = {ROLE: ['activityKindMdmId', 'customerMdmId', 'tin', 'businessRegDate']}
# словарь параметров модели
dictionaryModel = {'modelParameters': ['cnt_term_12','active_time','sum_any_12','cnt_any_12']}
dictionaryPimModelResult = {'pimModelResult': ['customerId']}
dictionaryPimModelParameters = {'modelParameters': ['customers_44fz_db','cnt_end_12_db','cnt_term_12_db','cnt_new_12_db','active_time_db','sum_any_12_db','cnt_any_12_db','sum_new_12_db', 'db_match_db', 'inn','productkindcd','sum_new_12_2sal', 'pricerur','end2new','duration','okpd_code_nom','cur2sal','sup_has_cust_region','sup_age','cnt_term_12','active_time', 'okved2_nom','is_new_customer','cur2mean_sum_12_any','score','pd','sum_new_12_2sal_score','pricerur_score','end2new_score','duration_score', 'okpd_code_nom_score', 'cur2sal_score', 'sup_has_cust_region_score', 'sup_age_score','cnt_term_12_score','active_time_score','okved2_nom_score', 'is_new_customer_score','cur2mean_sum_12_any_score','modelApplyDt']}

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
            if (k == 'roles' and v is not None) and ROLE in v:
                for i in dictionaryLegal[ROLE]:
                    resultList.append(d[i])

                for param in dictionaryModel['modelParameters']:
                    paramValue = ""
                    for x in d['modelResult']:
                        for y in x['modelParameters']:
                            if y['parameterName'] == param:
                                paramValue = y['parameterValue']
                    resultList.append(paramValue)

        return {k: v for k, v in ((k, getBorrowerParameters(v)) for k, v in d.items())}

def getBorrowerPimParameters(d):
    if not isinstance(d, (dict, list)): return d
    elif isinstance(d, list): return [v for v in (getBorrowerPimParameters(v) for v in d)]
    else:
        for k, v in d.items():

            # Просматриваем роли и находим нужную модель
            if k == 'pimModelResult' and v is not None:
                for pimModel in d['pimModelResult']:
                    if pimModel['modelId'] == MODEL:
                        for modelParam in dictionaryPimModelResult['pimModelResult']:
                            resultList.append(pimModel[modelParam])

                        for param in dictionaryPimModelParameters['modelParameters']:
                            paramValue = ""
                            for y in pimModel['modelParameters']:
                                if y['parameterName'] == param:
                                    paramValue = y['parameterValue']
                            resultList.append(paramValue)

        return {k: v for k, v in ((k, getBorrowerPimParameters(v)) for k, v in d.items())}

def getHeadersModel(header):
    # Формируем заголовки
    for i, j in dictionaryApp.items():
        for t in j:
            header.append(t)

    for i, j in dictionaryLegal.items():
        for t in j:
            header.append(t)

    for i, j in dictionaryModel.items():
        for t in j:
            header.append(t)
    return header

def getHeadersPimModel(header):
    # Формируем заголовки
    for i, j in dictionaryPimModelResult.items():
        for t in j:
            header.append(t)

    for i, j in dictionaryPimModelParameters.items():
        for t in j:
            header.append(t)
    return header

# По всем файлам JSON папке file_path_from
for entry in os.scandir(file_path_from):
    if entry.is_file() and entry.name.endswith('.json'):
        # Загружаем файл JSON
        with open(file_path_from + entry.name, encoding='utf-8') as fh:
            resultList = []
            #to_json = getBorrowerParameters(json.load(fh)) # Для исходных данных
            to_json = getBorrowerPimParameters(json.load(fh)) # Для результатов модели
            csvList.append(resultList)


#header = getHeadersModel([]) # Для исходных данных
header = getHeadersPimModel([]) # Для результатов модели

# формируем CSV
with open(file_path_to, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(csvList)
