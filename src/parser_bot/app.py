import asyncio

import loguru
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from tofunft_bot.src.parser_bot.price import get_last_price, parsing_floor_price, set_last_price
from data import TOKEN

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['текущая цена', 'парсинг лучшей цены']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Чего желаете ?', reply_markup=keyboard)


@dp.message_handler(Text(equals='текущая цена'))
async def get_lasted_price(message: types.Message):
    await message.answer(f'Текущая цена : {await get_last_price()}')


@dp.message_handler(Text(equals='парсинг лучшей цены'))
async def search_price(message: types.Message):
    while True:
        await asyncio.sleep(0.1)
        low = await parsing_floor_price()
        if low != await get_last_price():
            await message.answer(f'Самая низкая цена : {low}')
            await set_last_price(low)


def main():
    try:
        executor.start_polling(dp)
    except ValueError as ex:
        loguru.logger.error(ex)


if __name__ == '__main__':
    main()
