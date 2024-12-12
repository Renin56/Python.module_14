from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb = ReplyKeyboardMarkup(   # создаем основную клавиатуру
    keyboard=[
        [KeyboardButton(text='Регистрация')],   # добавляем кнопку в первый ряд
        [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Купить')],     # добавляем две кнопки во второй ряд
        [KeyboardButton(text='Информация')]  # добавление кнопки в третий ряд
    ], resize_keyboard=True     # подгон размера клавиатуры в зависимости от размера рабочего окна
)


inline_kb = InlineKeyboardMarkup(   # создание inline клавиатуры
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')]     # добавление кнопок
    ]
)


inline_kb_product = InlineKeyboardMarkup(   # создание inline клавиатуры
    inline_keyboard=[
        [InlineKeyboardButton(text='Product 1', callback_data='product_buying'),
         InlineKeyboardButton(text='Product 2', callback_data='product_buying')],   # добавление двух кнопок в первый ряд

        [InlineKeyboardButton(text='Product 3', callback_data='product_buying'),
         InlineKeyboardButton(text='Product 4', callback_data='product_buying')]    # добавление двух кнопок во второй ряд
    ]
)
