from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from texts import t_system, t_user, t_user_handlers, t_admin_handlers
from keyboards import kb_admin_main_menu, kb_user_main_menu
from users_functions import add_admin_rights
from filters.f_chat_type import ChatTypeFilter
from filters.f_users import IsUserFilter, IsAdminFilter

from config import ADMIN_PASS



class User_status(StatesGroup):
    pass_waiting = State()
    standart = State()

router = Router()
router.message.filter(
    ChatTypeFilter(chat_type="private"),
    IsUserFilter(),
    IsAdminFilter(is_admin=False)
)

@router.callback_query(F.data == t_system.back_user_callback)
async def start_menu_kb(callback: CallbackQuery, state: FSMContext):
    """ Выводит клавиатуру главного меню для пользователя без прав администратора. Отзывается на callback. """
    await state.clear()
    await callback.message.edit_text(text=t_user_handlers.main_menu_head, reply_markup=kb_user_main_menu.menu)

@router.message(Command("home"))
async def start_menu_cmd(msg: Message, state: FSMContext):
    """ Выводит клавиатуру главного меню для пользователя без прав администратора. Отзывается на команду. """
    await state.clear()
    await msg.answer(text=t_user_handlers.main_menu_head, reply_markup=kb_user_main_menu.menu)

@router.callback_query(F.data == t_user_handlers.authorization)
async def start_authorization(callback: CallbackQuery, state: FSMContext):
    """ 
    Вводит бота в режим ожидания пароля для получения прав админа.
    Выводит клавиатуру для выхода в главное меню.
    """
    sent_message = await callback.message.edit_text(
        text=t_user_handlers.ask_password,
        reply_markup=kb_user_main_menu.authorization_menu
    )
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await state.update_data(chat_id=chat_id, message_id=message_id)
    await state.set_state(User_status.pass_waiting)

@router.message(
    F.text,
    User_status.pass_waiting
)
async def do_authorization(msg: Message, bot: Bot, state: FSMContext):
    """ Принимает и сверяет пароль введеный пользователем во время авторизации. """
    id_data = await state.get_data()
    if msg.text != ADMIN_PASS:
        await bot.delete_message(chat_id=id_data["chat_id"], message_id=id_data["message_id"])
        await msg.answer(text=t_user.wrong_pass)
        await msg.delete()
        await msg.answer(
        text=t_user_handlers.ask_password,
        reply_markup=kb_user_main_menu.authorization_menu
    )
    elif msg.text == ADMIN_PASS:
        await bot.delete_message(chat_id=id_data["chat_id"], message_id=id_data["message_id"])
        await msg.answer(add_admin_rights(msg.from_user.id))
        await msg.delete()
        await msg.answer(text=t_admin_handlers.main_menu_head, reply_markup=kb_admin_main_menu.menu)
    