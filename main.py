import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, TIME_SET
from handlers import router, send_report_to_chat


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_report_to_chat, trigger=TIME_SET["trigger"], day_of_week=TIME_SET["day_of_week"], hour=TIME_SET["hour"], minute=TIME_SET["minute"], timezone=TIME_SET["timezone"], kwargs={"bot":bot})
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())