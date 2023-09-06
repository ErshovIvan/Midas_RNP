import gspread
import datetime

from config import *



gc = gspread.service_account(GOOGLE_CONF)
sh = gc.open(SH_NAME)
wrk_guide = sh.worksheet(REFERENCE)
wrk_data = sh.worksheet(VAULT)


# Возвращает словарь, где k - Ф.И. менеджера, v - словарь(k - название параметра, v - значение в конкретный день)
def get_all_managers_data(date):

    parameters_dict = {}
    for parameter in PARAMETERS:
        parameters_dict[parameter] = wrk_data.find(parameter).row-wrk_data.find(BEGINNING).row+1

    managers_list = wrk_guide.col_values(1)[1:]
    
    all_managers_data = {}

    for manager in managers_list:
        start_cell = wrk_data.find(f"{manager} start")
        date_cell = wrk_data.find(f"{date}")
        manager_data = {}
        for parameter, delta in parameters_dict.items():
            manager_data[parameter] = wrk_data.cell(start_cell.row+delta, date_cell.col).value
        all_managers_data[manager] = manager_data

    return(all_managers_data)


# Возвращает отформатированный отчет одной строкой, используя словарь из функции get_all_managers_data()
def make_today_report():

    report_date = datetime.datetime.today().strftime('%d.%m') # Записывает актуальную дату в переменную в формате ДД.ММ
    data_for_report = get_all_managers_data(report_date)
    report = f"\t{report_date}\n"

    for manager, data in data_for_report.items():
        report += f"\n{manager}"
        for parametr, value in data.items():
            report += f"\n{parametr}: {value}"
        report += f"\n"
    
    return(report)
