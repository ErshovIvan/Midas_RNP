from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts import t_gs_report, t_system



# Клавиатура с нопками выбора временных промежутков для формирования отчета GS.
gs_buttons = (
    [InlineKeyboardButton(text=t_gs_report.report_today, callback_data=t_gs_report.report_today)],
    [InlineKeyboardButton(text=t_gs_report.report_yesterday, callback_data=t_gs_report.report_yesterday)],
    [InlineKeyboardButton(text=t_gs_report.report_last_week, callback_data=t_gs_report.report_last_week)],
    [InlineKeyboardButton(text=t_system.cancel, callback_data=t_system.back_admin_callback)],
)

report_range = InlineKeyboardMarkup(inline_keyboard=gs_buttons)