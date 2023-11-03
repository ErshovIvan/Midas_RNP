from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts import t_admin_handlers


# Клавиатура - главное меню админа.
admin_menu_buttons = (
    [InlineKeyboardButton(text=t_admin_handlers.gs_report, callback_data=t_admin_handlers.gs_report)],
    [InlineKeyboardButton(text=t_admin_handlers.gpt_report, callback_data=t_admin_handlers.gpt_report)],
    [InlineKeyboardButton(text=t_admin_handlers.gpt_ask, callback_data=t_admin_handlers.gpt_ask)],

)

menu = InlineKeyboardMarkup(inline_keyboard=admin_menu_buttons)