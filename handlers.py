from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from config import CHAT_ID

import gs



router = Router()

@router.message(Command("report"))
async def send_report(msg: Message):
    await msg.answer(gs.make_today_report())


async def send_report_to_chat(bot: Bot):
    await bot.send_message(CHAT_ID, gs.make_today_report())