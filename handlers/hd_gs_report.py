from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import CHAT_ID, S_GROUP_ID, S_GROUP_THREAD

import gs
from texts import t_admin_handlers, t_gs_report, t_system
from keyboards import kb_gs_report
from filters.f_chat_type import ChatTypeFilter
from filters.f_users import IsUserFilter



class GsReportStatus(StatesGroup):
    gs_report_range_geted = State()
    

router = Router()
router.message.filter(
    ChatTypeFilter(chat_type="private"),
    IsUserFilter()
)

@router.callback_query(F.data == t_admin_handlers.gs_report)
async def gs_report_range_kb(callback: CallbackQuery, state: FSMContext):
    """ Выводит клавиатуру с выводом временных диапазонов для данных из РНП. """
    await callback.message.edit_text(text=t_gs_report.report_range, reply_markup=kb_gs_report.report_range)
    await state.set_state(GsReportStatus.gs_report_range_geted)

@router.callback_query(
    F.data.in_(t_gs_report.range_callback_list),
    GsReportStatus.gs_report_range_geted
)
async def send_gs_report(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """ Выводит отчет РНП """
    await callback.message.delete()
    sent_message = await callback.message.answer(t_system.report_in_progress)
    message_id = sent_message.message_id
    chat_id = sent_message.chat.id
    await state.update_data(report_range=callback.data)
    report_data = await state.get_data()

    if report_data["report_range"] == t_gs_report.report_today:
        await bot.edit_message_text(text=gs.make_today_report(), message_id=message_id, chat_id=chat_id)
        await bot.send_message(text=t_gs_report.report_range, reply_markup=kb_gs_report.report_range, chat_id=chat_id)

    elif report_data["report_range"] == t_gs_report.report_yesterday:
        await bot.edit_message_text(text=gs.make_yesterday_report(), message_id=message_id, chat_id=chat_id)
        await bot.send_message(text=t_gs_report.report_range, reply_markup=kb_gs_report.report_range, chat_id=chat_id)

    elif report_data["report_range"] == t_gs_report.report_last_week:
        await bot.edit_message_text(gs.make_last_week_report(), message_id=message_id, chat_id=chat_id)
        await bot.send_message(text=t_gs_report.report_range, reply_markup=kb_gs_report.report_range, chat_id=chat_id)



async def send_daily_report_to_chat(bot: Bot):
    """ Выводит сегодняшний отчет РНП в групповой чат. """
    await bot.send_message(CHAT_ID, gs.make_today_report())


async def send_weekly_report_to_chat(bot: Bot):
    """ Выводит отчет РНП за последние 7 дней в групповой чат. """
    await bot.send_message(CHAT_ID, gs.make_last_week_report())


# Тест
async def send_daily_report_to_s_group(bot: Bot):
    """ Выводит сегодняшний отчет РНП в супер группу. """
    await bot.send_message(chat_id=S_GROUP_ID, message_thread_id=S_GROUP_THREAD, text=gs.make_today_report())


async def send_weekly_report_to_s_group(bot: Bot):
    """ Выводит отчет РНП за последние 7 дней в супер группу. """
    await bot.send_message(chat_id=S_GROUP_ID, message_thread_id=S_GROUP_THREAD, text=gs.make_today_report())