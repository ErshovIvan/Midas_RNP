import gspread
import datetime

from config import *



gc = gspread.service_account(GOOGLE_CONF)
sh = gc.open(SH_NAME)
wrk_guide = sh.worksheet(REFERENCE)
wrk_data = sh.worksheet(GUIDE)



def get_data(date_list: list) -> dict:
    """
    Вытаскивает всю необходимую информацию из гугл-таблицы за указанную дату/диапазон дат и форматирует в словарь
    {manager_name1: {block1:{parameter1: value1, parameter2: value2}, block2:{parameter3: value3},...}
    """

    data = wrk_data.get_all_values()
    
    for row in data: # Ищется первая строка содержащая "HEADS" и получается ее индекс для дальнейшего форматирования данных.
        if HEADS_COL_NAME in row:
            head_cell_row_index = data.index(row)
            break
    
    # Данные форматируются. Данные на входе: Список, каждый элемент которого - список всех ячеек в строке.
    # Данные на выходе: Словарь, где ключ - значение ячейки строки с датами ('%dd.%mm'), а значения все остальные ячейки столбца.
    data_dict = {}
    len_of_row = len(data[0])
    for col_num in range(len_of_row): 
        col_value_list = []
        for row in data:
            col_value_list.append(row[col_num])
        key_name = data[head_cell_row_index][col_num]
        data_dict[key_name] = col_value_list

    # В этом блоке с листа "СПРАВОЧНИК" формируется список с ФИ МОПов при условии активного флажка в столбце "МОП ТГ БОТ"
    guide_data = wrk_guide.get_all_values() 
    managers_names_col_index = guide_data[0].index(GUIDE_MANAGERS_NAMES_COL)
    managers_config_col_index = guide_data[0].index(GUIDE_MANAGERS_CONFIG_COL)
    managers_list = []
    for row in guide_data:
        if row[managers_names_col_index] != '' and row[managers_config_col_index] == 'TRUE':
            managers_list.append(row[managers_names_col_index])

    # Данные ищутся и суммируются по дням в соответсвии с ФИ МОПа, названием блока и параметра        
    managers_data ={}
    for manager in managers_list:
        block_data = {}
        manager_head_index = data_dict[HEADS_COL_NAME].index(f'{manager} start')
        end_index = len(data_dict[HEADS_COL_NAME])
        for block_name, block_parameters in PARAMETERS.items():
            parameters_value = {}
            for parameter in block_parameters:
                for row_index in range(manager_head_index, end_index): # Перебираем числа (индекс строки) от "{Фамилия Имя менеджера} start" и до конца файла
                    if data_dict[HEADS_COL_NAME][row_index] == parameter and data_dict[BLOCK_COL_NAME][row_index] == block_name: # Проверка по названию параметри и названию блока
                        parameter_value = 0
                        for day in date_list:
                            if data_dict[day][row_index] != "":
                                parameter_value += int(data_dict[day][row_index])
                            else:
                                continue
                        parameters_value[parameter] = parameter_value
                        break
                    else:
                        continue
            block_data[block_name] = parameters_value
        managers_data[manager] = block_data
    
    return(managers_data)


    
def make_report(date_list: list) -> str:
    """
    Словарь с данными по кажому менеджеру форматируется в одну строку
    """

    # Если отчет вулючает 2 и больше даты, то в шапке "отчета" указываются первый и последний элемент списка дат.
    managers_data = get_data(date_list)
    if len(date_list) == 1:
        report = f"\n\tРезультаты за <b>{date_list[0]}</b>" 
    else:
        report = f"\n\tРезультаты за <b>{date_list[0]} - {date_list[-1]}</b>"

    # Формирует словарь total с нулевыми показателями для всех искомых парамитров, для дальнейшего рассчета суммы по менеджерам
    parameters_total = {}
    for block_name, parameters_list in PARAMETERS.items():
        block = {}
        for parameter_name in parameters_list:
            block[parameter_name] = 0
        parameters_total[block_name] = block          

    # Передает данные по менеджерам в "отчет" по порядку.
    # **{manager_name}**
    # {parameter1_name}: {parameter1_value}
    # {parameter2_name}: {parameter2_value}...
    # Так-же добавляет значения каждого менеджера к соответствующему параметру в словарь total 
    for manager_name, manager_values in managers_data.items():
        report += f"\n\n<b>{manager_name}</b>"
        for block_name, block_value in manager_values.items():
            for parameter_name, parameter_value in block_value.items():
                report += f"\n{parameter_name}: {parameter_value}"
                parameters_total[block_name][parameter_name] += parameter_value
    
    # Добавляет в конец отчета словарь total
    # **{block1}**
    # {paramete_name1}: {parameter1_value}
    # **{block2}**
    report += f"\n"
    for block_name, block_value in parameters_total.items():
        if bool(block_value):
            report += f"\n<b>{block_name}</b>"
        for parameter_name, parameter_value in block_value.items():
            report += f"\n{parameter_name}: {parameter_value}"

    return(report)


def make_today_report() -> str:
    """
    Запускает создание очтета за сегодняшнее число
    """
    today_date = []
    today_date.append(datetime.datetime.today().strftime('%d.%m'))
    report = make_report(today_date)
    return(report)



def make_yesterday_report() -> str:
    """
    Запускает создание отчета за вчера
    """
    yesterday_date = []
    yesterday_date.append((datetime.datetime.today()-datetime.timedelta(days=1)).strftime('%d.%m'))
    report = make_report(yesterday_date)
    return(report)


def make_last_week_report() -> str:
    """
    Запускает создание отчета за диапазон дат: (today-7days) по (today-1day). Условно за прошлую неделю.
    """
    #last_monday_date = (datetime.datetime.today()-datetime.timedelta(days=7)).strftime('%d.%m')
    last_week_days = []
    for i in range(1, 8):
        last_week_day = (datetime.datetime.today()-datetime.timedelta(days=i)).strftime('%d.%m')
        last_week_days.insert(0, last_week_day)
    report = make_report(last_week_days)
    return(report)
