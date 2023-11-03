from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


import chat_gpt
from texts import t_gpt_report, t_gs_report, t_system
from texts import t_admin_handlers
from keyboards import kb_gpt_report
from filters.f_chat_type import ChatTypeFilter
from filters.f_users import IsAdminFilter



class GptReportStatus(StatesGroup):
    gpt_report_range_geted = State()
    gpt_report_type_geted = State()
    free_prompt_waiting = State()


router = Router()
router.message.filter(
    ChatTypeFilter("private"),
    IsAdminFilter()
)


@router.callback_query(F.data == t_admin_handlers.gpt_report)
@router.callback_query(F.data == t_gpt_report.back3_2)
async def gpt_report_range(callback: CallbackQuery, state: FSMContext):
    """ Выводит клавиатуру с выводом временных диапазонов для данных из РНП. """
    await callback.message.edit_text(t_gs_report.report_range, reply_markup=kb_gpt_report.report_range)
    await state.set_state(GptReportStatus.gpt_report_range_geted)

@router.callback_query(
    F.data.in_(t_gs_report.range_callback_list),
    GptReportStatus.gpt_report_range_geted
)
async def gpt_report_type(callback: CallbackQuery, state: FSMContext):
    """ Выводит клавиатуру для выбора типа промпта. Отзывается на callback из предыдущего меню. """
    await state.update_data(report_range = callback.data)
    await callback.message.edit_text(text=t_gpt_report.report_type, reply_markup=kb_gpt_report.report_type)
    await state.set_state(GptReportStatus.gpt_report_type_geted)

@router.callback_query(F.data == t_gpt_report.back4_3)
async def gpt_report_type(callback: CallbackQuery, state: FSMContext):
    """ Выводит клавиатуру для выбора типа промпта. Отзывается на callback из последующего меню. """
    await callback.message.edit_text(text=t_gpt_report.report_type, reply_markup=kb_gpt_report.report_type)
    await state.set_state(GptReportStatus.gpt_report_type_geted)

@router.callback_query(
    F.data.in_(t_gpt_report.type_callback_list),
    GptReportStatus.gpt_report_type_geted
)
async def send_gpt_report(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """ Выводит отет ChatGPT на заготовленный промпт. """
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await state.update_data(report_type = callback.data)
    report_data  = await state.get_data()
    sent_message = await callback.message.answer(t_system.report_in_progress)
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await bot.edit_message_text(chat_gpt.make_gpt_request(report_data), chat_id=chat_id, message_id=message_id)
    await bot.send_message(text=t_gpt_report.report_type, reply_markup=kb_gpt_report.report_type, chat_id=chat_id)

@router.callback_query(
    F.data == t_gpt_report.free_prompt,
    GptReportStatus.gpt_report_type_geted
)
async def gpt_asking_prompt(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """ Ожидает ввода рукописного промпта. Выводит клавиатуру для возврата. """
    sent_message = await callback.message.edit_text(
        text=t_gpt_report.free_prompt_menu_head,
        reply_markup=kb_gpt_report.free_prompt_menu
    )
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await state.update_data(chat_id=chat_id, message_id=message_id)
    await state.set_state(GptReportStatus.free_prompt_waiting)
    
@router.message(
    F.text,
    GptReportStatus.free_prompt_waiting
)
async def send_free_prompt_report(msg: Message, bot: Bot, state: FSMContext):
    """ Выводит ответ ChatGPT на рукописный промпт. """
    data = await state.get_data()
    await bot.delete_message(chat_id=data["chat_id"], message_id=data["message_id"])
    sent_message = await msg.answer(text=t_system.report_in_progress)
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await bot.edit_message_text(
        text=chat_gpt.make_gpt_free_prompt_request(
            free_prompt=msg.text,
            report_data=data["report_range"]
        ),
        chat_id=chat_id,
        message_id=message_id
    )
    sent_message = await bot.send_message(
        text=t_gpt_report.free_prompt_menu_head,
        reply_markup=kb_gpt_report.free_prompt_menu,
        chat_id=chat_id
    )
    chat_id = sent_message.chat.id
    message_id = sent_message.message_id
    await state.update_data(chat_id=chat_id, message_id=message_id)