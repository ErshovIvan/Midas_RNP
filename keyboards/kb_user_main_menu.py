from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts import t_system, t_user_handlers



# Клавиатура - главное меню простого юзера.
user_menu_buttons = (
    [InlineKeyboardButton(text=t_user_handlers.authorization, callback_data=t_user_handlers.authorization)],
)

menu = InlineKeyboardMarkup(inline_keyboard=user_menu_buttons)

# Клавиатура подменю получения прав админа. Кнопка возрата в главное меню юзера.
authorization_menu_buttons = (
    [InlineKeyboardButton(text=t_system.cancel, callback_data=t_system.back_user_callback)],
)

authorization_menu = InlineKeyboardMarkup(inline_keyboard=authorization_menu_buttons)