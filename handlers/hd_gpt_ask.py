from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


import chat_gpt
from texts import t_system
from texts import t_admin_handlers, t_gpt_ask
from keyboards import kb_gpt_ask
from filters.f_chat_type import ChatTypeFilter
from filters.f_users import IsAdminFilter



class GptAskStatus(StatesGroup):
    gpt_ask_waiting = State()

router = Router()
router.message.filter(
    ChatTypeFilter("private"),
    IsAdminFilter()
)

@router.callback_query(
    F.data == t_admin_handlers.gpt_ask
)
async def gpt_waiting_question(callback: CallbackQuery, state: FSMContext):
    """
    Активирует ожидание сообщения от пользователя, которое будет передано ChatGPT.
    Выводит клавиатуру для возврата в меню.
    """
    sent_message = await callback.message.edit_text(text=t_gpt_ask.menu_head, reply_markup=kb_gpt_ask.ask_menu)
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await state.update_data(chat_id=chat_id, message_id=message_id)
    await state.set_state(GptAskStatus.gpt_ask_waiting)

@router.message(
    F.text,
    GptAskStatus.gpt_ask_waiting
)
async def gpt_answer(msg: Message, bot: Bot, state: FSMContext):
    """ Выводит ответ от ChatGPT. """
    id_data = await state.get_data()
    await bot.delete_message(chat_id=id_data["chat_id"], message_id=id_data["message_id"])
    sent_message = await msg.answer(text=t_system.answer_in_progress)
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    prompt = msg.text
    await bot.edit_message_text(text=chat_gpt.call_ai(prompt), chat_id=chat_id, message_id=message_id)
    sent_message = await bot.send_message(text=t_gpt_ask.menu_head, reply_markup=kb_gpt_ask.ask_menu, chat_id=chat_id)
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await state.update_data(chat_id=chat_id, message_id=message_id)