import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, TIME_SET_DAILY, TIME_SET_WEEKLY
import handlers.hd_gs_report as hd_gs_report
import handlers.hd_gpt_report as hd_gpt_report
import handlers.hd_gpt_ask as hd_gpt_ask
import handlers.hd_user as hd_user
import handlers.hd_start as hd_start
import handlers.hd_admin as hd_admin


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        hd_admin.router,
        hd_user.router,
        hd_gs_report.router,
        hd_gpt_report.router,
        hd_gpt_ask.router,
        hd_start.router
    )
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        hd_gs_report.send_daily_report_to_s_group,
        trigger=TIME_SET_DAILY["trigger"],
        day_of_week=TIME_SET_DAILY["day_of_week"],
        hour=TIME_SET_DAILY["hour"],
        minute=TIME_SET_DAILY["minute"],
        timezone=TIME_SET_DAILY["timezone"],
        kwargs={"bot":bot}
    )

    scheduler.add_job(
        hd_gs_report.send_weekly_report_to_s_group,
        trigger=TIME_SET_WEEKLY["trigger"],
        day_of_week=TIME_SET_WEEKLY["day_of_week"],
        hour=TIME_SET_WEEKLY["hour"],
        timezone=TIME_SET_WEEKLY["timezone"],
        kwargs={"bot":bot}
    )

    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())