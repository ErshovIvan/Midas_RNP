import gspread
import datetime

from config import *



gc = gspread.service_account(GOOGLE_CONF)
sh = gc.open(SH_NAME)
wrk_guide = sh.worksheet(REFERENCE)
wrk_data = sh.worksheet(VAULT)


def get_data(date_list):

    data = wrk_data.get_all_values()
    managers_list = wrk_guide.col_values(1)[1:]

    head_cell_row = wrk_data.find(START_CELL).row-1
    data_dict = {}
    len_of_row = len(data[0])

    for col_num in range(len_of_row): # Данные с гугл таблици форматируются в словар (k - название столбца, v - список со всеми значениями)
        col_value_list = []
        for row in data:
            col_value_list.append(row[col_num])
        key_name = data[head_cell_row][col_num]
        data_dict[key_name] = col_value_list

    heads_list = data_dict[START_CELL]
    managers_data = {}

    for manager in managers_list:
        one_manager_data = {}
        manager_start = heads_list.index(f'{manager} start')
        manager_end = heads_list.index(f'{manager} end')
        
        for parameter in PARAMETERS:
            for head_num in range(manager_start, manager_end):
                if heads_list[head_num] == parameter:
                    one_manager_data[parameter] = 0
                    for day in date_list:
                        values_on_date_list = data_dict[day]
                        one_manager_data[parameter] += int(values_on_date_list[head_num])
        managers_data[manager] = one_manager_data
    
    return(managers_data)


def make_report(date_list):

    managers_data = get_data(date_list)
    if len(date_list) == 1:
        report = f"\n\tРезультаты за {date_list[0]}" # Форматирует ежедневный отчет в одну строку
    else:
        report = f"\n\tРезультаты за {date_list[0]} - {date_list[-1]}"

    parameters_total = {}
    for parameter in PARAMETERS:
        parameters_total[parameter] = 0

    for manager_name, manager_values in managers_data.items():
        report += f"\n\n{manager_name}"
        for parameter_name, parameter_value in manager_values.items():
            report += f"\n{parameter_name}: {parameter_value}"
            parameters_total[parameter_name] += int(parameter_value)
    
    report += f"\n\nИТОГ"
    for parameter_name, parameter_value in parameters_total.items():
        report += f"\n{parameter_name}: {parameter_value}"

    return(report)


def make_today_report():
    today_date = []
    today_date.append(datetime.datetime.today().strftime('%d.%m'))
    report = make_report(today_date)
    return(report)



def make_last_week_report():
    #last_monday_date = (datetime.datetime.today()-datetime.timedelta(days=7)).strftime('%d.%m')
    last_week_days = []
    for i in range(1, 8):
        last_week_day = (datetime.datetime.today()-datetime.timedelta(days=i)).strftime('%d.%m')
        last_week_days.insert(0, last_week_day)
    report = make_report(last_week_days)
    return(report)