from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.f_users import IsUserFilter
from filters.f_chat_type import ChatTypeFilter
from users_functions import add_new_user
from texts import t_user_handlers
from keyboards import kb_user_main_menu



router = Router()
router.message.filter(
    ChatTypeFilter(chat_type="private"),
    IsUserFilter(is_user=False)    
)

@router.message(Command("start"))
async def adding_new_user(msg: Message):
    """ Добавляет user_id и имя пользователя в базу бота по команде /start. """
    await msg.answer(add_new_user(msg.from_user.id, msg.from_user.full_name))
    await msg.answer(text=t_user_handlers.main_menu_head, reply_markup=kb_user_main_menu.menu)