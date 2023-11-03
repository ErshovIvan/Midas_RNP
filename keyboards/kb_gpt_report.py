from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts import t_gpt_report, t_gs_report, t_system



# Клавиатура с выбором временного промежутка GS отчета
# для дальнейшей обработки через ChatGPT.
# Есть кнопка возврата в главное меню админа.
report_range_buttons = (
    [InlineKeyboardButton(text=t_gs_report.report_today, callback_data=t_gs_report.report_today)],
    [InlineKeyboardButton(text=t_gs_report.report_yesterday, callback_data=t_gs_report.report_yesterday)],
    [InlineKeyboardButton(text=t_gs_report.report_last_week, callback_data=t_gs_report.report_last_week)],
    [InlineKeyboardButton(text=t_system.cancel, callback_data=t_system.back_admin_callback)],
)
report_range = InlineKeyboardMarkup(inline_keyboard=report_range_buttons)

# Клавиатура с выбором типа промпта ([заготовленные]/свободный) для совмещения с отчетом GS.
# Есть кнопки возврата в главное меню админа и возврата в меню с выбором временных промежутков(назад).
report_type_buttons = (
    [InlineKeyboardButton(text=t_gpt_report.analysis, callback_data=t_gpt_report.analysis)],
    [InlineKeyboardButton(text=t_gpt_report.anomaly, callback_data=t_gpt_report.anomaly)],
    [InlineKeyboardButton(text=t_gpt_report.recommendations, callback_data=t_gpt_report.recommendations)],
    [InlineKeyboardButton(text=t_gpt_report.free_prompt, callback_data=t_gpt_report.free_prompt)],
    [InlineKeyboardButton(text=t_system.cancel, callback_data=t_system.back_admin_callback),
     InlineKeyboardButton(text=t_system.back, callback_data=t_gpt_report.back3_2)
     ],
)
report_type = InlineKeyboardMarkup(inline_keyboard=report_type_buttons)

# Клавиатура с кнопками возврата в главное меню админа и возврата в меню выбора промпта.
free_prompt_menu_buttons = (
    [
        InlineKeyboardButton(text=t_system.cancel, callback_data=t_system.back_admin_callback),
        InlineKeyboardButton(text=t_system.back, callback_data=t_gpt_report.back4_3)        
    ],
)

free_prompt_menu = InlineKeyboardMarkup(inline_keyboard=free_prompt_menu_buttons)