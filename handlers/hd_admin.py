from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from filters.f_chat_type import ChatTypeFilter
from filters.f_users import IsUserFilter, IsAdminFilter
from texts import t_admin_handlers, t_system
from keyboards import kb_admin_main_menu



router = Router()
# Фильтры на личные сообщения и права админа
router.message.filter(
    ChatTypeFilter("private"),
    IsUserFilter(),
    IsAdminFilter()
)

# Вызов главного меню для админа
@router.callback_query(F.data == t_system.back_admin_callback)
async def full_menu_kb(callback: CallbackQuery, state: FSMContext):
    """ Выводит клавиатуру главного меню. Отзывается на callback. """
    await state.clear()
    await callback.message.edit_text(text=t_admin_handlers.main_menu_head, reply_markup=kb_admin_main_menu.menu)

@router.message(Command("home"))
async def full_menu_cmd(msg: Message, state: FSMContext):
    """ Выводит клавиатуру главного меню. Отзывается на команду. """
    await state.clear()
    await msg.answer(text=t_admin_handlers.main_menu_head, reply_markup=kb_admin_main_menu.menu)