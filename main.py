import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
 KeyboardButton,
 Message,
 ReplyKeyboardMarkup,
 ReplyKeyboardRemove,
 )

TOKEN = getenv("6266404942:AAFKyd6fYXjmbiwrBLLN3sYBN6-B9NpiBUI")

form_router = Router()


class States(StatesGroup):
    start = State()

    quit = State()




@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(States.start)
    await message.answer(
    "Привет, как тебя зовут?",
        reply_markup=ReplyKeyboardRemove(),
)

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
