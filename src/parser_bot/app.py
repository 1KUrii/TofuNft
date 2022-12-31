import asyncio

import loguru
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from tofunft_bot.src.parser_bot.price import get_current_price, parse_lowest_price, set_current_price
from data import TOKEN

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['current price', 'parse lowest price']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('What you want ?', reply_markup=keyboard)


@dp.message_handler(Text(equals='current price'))
async def get_lasted_price(message: types.Message):
    await message.answer(f'current price : {await get_current_price()}')


@dp.message_handler(Text(equals='parse lowest price'))
async def search_price(message: types.Message):
    while True:
        await asyncio.sleep(0.1)
        low = await parse_lowest_price()
        if low != await get_current_price():
            await message.answer(f'parse lowest price : {low}')
            await set_current_price(low)


def main():
    try:
        executor.start_polling(dp)
    except ValueError as ex:
        loguru.logger.error(ex)


if __name__ == '__main__':
    main()
