from aiogram import Router, F, types

from src.utils import build_answer

source_router = Router()

@source_router.message(F.text)
async def get_request(msg: types.Message):
    answer = await build_answer(msg.text)
    await msg.answer(answer)