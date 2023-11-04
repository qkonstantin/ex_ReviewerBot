import asyncio
import logging
import sys

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

TOKEN = "6266404942:AAFKyd6fYXjmbiwrBLLN3sYBN6-B9NpiBUI"

form_router = Router()


class States(StatesGroup):
    start = State()
    name = State()
    like_bots = State()
    quit = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(States.name)  # Set the state to 'name' state
    await message.answer(
        "Привет, как тебя зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(States.name)
async def process_name(message: Message, state: FSMContext) -> None:
    async with state as data:
        data['name'] = message.text

    await States.like_bots.set()  # Set the state to 'like_bots' state
    await message.answer(f"Приятно познакомиться, {message.text}! Нравится ли тебе писать ботов? (Да / Нет)")


@form_router.message(States.like_bots)
async def process_like_bots(message: Message, state: FSMContext) -> None:
    async with state as data:
        name = data.get('name')

    if message.text.lower() == 'да':
        await message.answer(f"Отлично, {name}! Удачи в разработке ботов!")
    else:
        await message.answer(f"Понятно, {name}. Может, в будущем попробуешь написать бота?")

    await state.finish()  # Finish the state machine




async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
