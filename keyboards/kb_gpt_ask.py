from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts import  t_system


# Меню всплывающее во время ручного ввода запроса для ChatGPT с кнопкой возрата в главное меню админа.
ask_menu_buttons = (
    [InlineKeyboardButton(text=t_system.cancel, callback_data=t_system.back_admin_callback)],
)
ask_menu = InlineKeyboardMarkup(inline_keyboard=ask_menu_buttons)