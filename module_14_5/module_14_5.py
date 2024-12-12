########################################################################################################################
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
########################################################################################################################

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from crud_functions import *
from module_14_5_keybord import *
from transliterate import translit  # транслитерация русского текста в латинский
from config import *

########################################################################################################################

logging.basicConfig(level=logging.INFO, filemode='a', filename='PyAiogram2bot.log', encoding='utf-8',
                    format='%(asctime)s | %(levelname)s | %(message)s')

########################################################################################################################

TOKEN = TOKEN

########################################################################################################################

# создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)  # создаем бот
dp = Dispatcher(bot, storage=MemoryStorage())   # создание диспетчера

########################################################################################################################

initial_db()  # создаем БД
initial_data()  # заполняем данными

########################################################################################################################

products = get_all_products()  # получаем содержимое БД

########################################################################################################################

# МАШИНА СОСТОЯНИЙ ДЛЯ РАСЧЕТА КАЛЛОРИЙ
class UserState(StatesGroup):
    age = State()   # возраст
    growth = State()    # рост
    weight = State()    # вес

# МАШИНА СОСТОЯНИЙ ДЛЯ РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ
class RegistrationState(StatesGroup):
    username = State()  # логин
    email = State()     # адрес электронной почты
    age = State()   # возраст
    balance = 1000  # баланс

########################################################################################################################

# НАЧАЛО РАБОТЫ С БОТОМ
@dp.message_handler(commands=['start'])     # реакция на команду /start
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup=kb)

########################################################################################################################

# НАЖАТА КНОПКА "РЕГИСТРАЦИЯ"
@dp.message_handler(text='Регистрация')     # реакция на текст сообщения "Регистрация"
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()  # ожидание ввода логина пользователя

# ввод имени пользователя
@dp.message_handler(state=RegistrationState.username)   # реакция на ввод логина
async def set_username(message, state):

    message.text = translit(message.text, language_code='ru', reversed=True)    # преобразование русских букв в латинские

    if not is_included(message.text):   # проверка существует ли вводимый логин в БД
        await state.update_data(username=message.text)  # обновление состояния в поле username
        await message.answer('Ведите свой email:')
        await RegistrationState.email.set()    # ожидание ввода адреса электронной почты
    else:
        await message.answer('Пользователь существует, введите другое имя:')
        await RegistrationState.username.set()  # ожидание ввода логина пользователя

# ввод электронной почты
@dp.message_handler(state=RegistrationState.email)  # реакция на ввод адреса электронной почты
async def set_email(message, state):
    await state.update_data(email=message.text)     # обновление состояния поля адреса электронной почты
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()   # ожидание ввода возраста

# ввод возраста и регистрация пользователя
@dp.message_handler(state=RegistrationState.age)    # реакция на ввод возраста
async def set_age(message, state):
    await state.update_data(age=message.text)   # обновление состояния поля возраст

    data = await state.get_data()   # сохранение всех данных
    msg = add_user(data['username'], data['email'], data['age'])    # сохранение в БД

    await message.answer(msg)
    await state.finish()    # завершение работы машины состояний

########################################################################################################################

# НАЖАТА КНОПКА "РАССЧИТАТЬ"
@dp.message_handler(text='Рассчитать')  # реакция на ввод текста "Рассчитать"
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)     # вывод inline клавиатуры

# нажата кнопка "Формула расчета"
@dp.callback_query_handler(text='formulas')     # реакция на нажатие кнопки с текстом "Формула"
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора \n Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')   # вывод сообщения
    await call.answer()     # завершение активности кнопки

# нажата кнопка "Рассчитать норму калорий"
@dp.callback_query_handler(text='calories')     # реакция на нажатие кнопки с текстом "Рассчитать норму калорий"
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()   # ожидание ввода возраста
    await call.answer()     # завершение активности кнопки

# ввод роста
@dp.message_handler(state=UserState.age)    # реакция на состояние ввода возраста
async def set_growth(message, state):
    await state.update_data(age=message.text)   # обновление данных поля возраст
    await message.answer('Введите свой рост:')
    await UserState.growth.set()    # ожидание ввода роста

# ввод веса
@dp.message_handler(state=UserState.growth)     # реакция на состояние ввода роста
async def set_weight(message, state):
    await state.update_data(growth=message.text)    # обновление данных поля рост
    await message.answer('Введите свой вес:')
    await UserState.weight.set()    # ожидание ввода веса

# расчет нормы калорий
@dp.message_handler(state=UserState.weight)     # реакция на состояние ввода веса
async def send_calories(message, state):
    await state.update_data(weight=message.text)    # обновление данных в поле вес

    data = await state.get_data()   # сохранение введенных данных
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 + int(data['age']) + 5     # расчет нормы калорий

    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()    # завершение работы машины состояния

########################################################################################################################

# НАЖАТА КНОПКА "ИНФОРМАЦИЯ"
@dp.message_handler(text='Информация')  # реакция на нажатие кнопки "Информация"
async def all_message(message):
    await message.answer('Информация о боте:\n'
                         'Текущая версия: 0.0.1\n'
                         '-----------------------------------\n'
                         'Тестовый бот созданный в рамках изучения темы асинхронного программирования '
                         'и создание ботов для телеграм на Python с помощью библиотеки aiogram2 (версия 2.25.1)!\n'
                         '-----------------------------------\n'
                         'Чтобы продолжить работу с ботом, введите /start')

########################################################################################################################

# НАЖАТА КНОПКА "КУПИТЬ"
@dp.message_handler(text='Купить')  # реакция на нажатие кнопки "Купить"
async def get_buying_list(message):
    for product in products:    # перебираем все полученные записи о продуктах
        # await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        with open(f'img/{product[1]}.jpg', 'rb') as img:    # открываем каждое изображение соответствующее продукту
            # await message.answer_photo(img)
            await message.answer_photo(img, f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb_product)   # вывод inline клавиатуры покупки продуктов

# покупка товара
@dp.callback_query_handler(text='product_buying')   # реакция на нажатие кнопки продукта
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()     # завершение активности кнопки

########################################################################################################################

if __name__ == '__main__':
    try:
        logging.info('Запуск PyAiogram2bot!')
        executor.start_polling(dp, skip_updates=True)
        logging.info('PyAiogram2bot остановлен!')
    except:
        print('Ошибка запуска PyAiogram2bot!')
        logging.warning('Ошибка запуска PyAiogram2bot!', exc_info=True)
