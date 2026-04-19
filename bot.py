import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, ai_chat, books, audio, about
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")
    
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(ai_chat.router)
    dp.include_router(books.router)
    dp.include_router(audio.router)
    dp.include_router(about.router)

    logger.info("G'afur G'ulom boti ishga tushmoqda...")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
