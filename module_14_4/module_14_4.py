####################################################################################################################
#
#   ОШИБКА
#
#   Проверка SSL сертификата при запуске бота
#
#   РЕШЕНИЕ
#
#   Нужно открыть папку с установленными пакетами, найти там папки: (Lib - site-packages - aiogram - bot)
#
#   Там будут 2 файла - это api.py и base.py.
#
#   В base.py найди строку
#       async with session.get(url, timeout=timeout, proxy=self.proxy, proxy_auth=self.proxy_auth) as response
#   и вставь в параметры ssl=False.
#
#   А в файле api.py - найди строку
#       async with session.post(url, data=req, **kwargs) as response
#   и аналогичным образом добавь в парамеры ssl=False.
#
####################################################################################################################


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
from config import *


logging.basicConfig(level=logging.INFO, filemode='a', filename='PyAiogram2bot.log', encoding='utf-8',
                    format='%(asctime)s | %(levelname)s | %(message)s')


TOKEN = TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

initial_db()  # создаем БД
initial_data()  # заполняем данными
products = get_all_products()  # получаем содержимое БД


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
        InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')]
    ]
)


inline_kb_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product 1', callback_data='product_buying'),
         InlineKeyboardButton(text='Product 2', callback_data='product_buying'),
         InlineKeyboardButton(text='Product 3', callback_data='product_buying'),
         InlineKeyboardButton(text='Product 4', callback_data='product_buying')]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        with open(f'img/{product[1]}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb_product)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    callories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 + int(data['age']) + 5

    await message.answer(f'Ваша норма калорий: {callories}')
    await state.finish()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора \n Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    try:
        logging.info('Запуск PyAiogram2bot!')
        executor.start_polling(dp, skip_updates=True)
        logging.info('PyAiogram2bot остановлен!')
    except:
        print('Ошибка запуска PyAiogram2bot!')
        logging.warning('Ошибка запуска PyAiogram2bot!', exc_info=True)
