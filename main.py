import asyncio

import logging

from aiogram import Bot, Dispatcher

from src.config import TOKEN

from src.bot import source_router

bot = Bot(token=TOKEN)

dp = Dispatcher()

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    dp.include_router(source_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())