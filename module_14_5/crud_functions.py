import sqlite3


def initial_db():
    connection = sqlite3.connect('database.db')     # подключение к БД
    cursor = connection.cursor()    # создание курсора для навигации по БД

    # создание таблицы Products если она отсутствует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL    
        )
        ''')

    # создание таблицы Users если она отсутствует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL    
        )
        ''')

    connection.commit()     # сохранение изменений
    connection.close()      # закрытие соединения


def is_included(username):
    connection = sqlite3.connect('database.db')     # подключение к БД
    cursor = connection.cursor()    # создание курсора для навигации по БД
    exist = False   # определение наличия / отсутствия записи

    cursor.execute('SELECT * FROM Users WHERE username=?', (username,)) # делаем запрос в БД на наличие пользователя по его логину
    if not (cursor.fetchone() is None): # если пользователь найден
        exist = True    # переключаем переключатель наличия записи

    connection.commit()     # сохранение изменений
    connection.close()      # закрытие соединения

    return exist    # вывод результата

def add_user(username, email, age):
    connection = sqlite3.connect('database.db')     # подключение к БД
    cursor = connection.cursor()    # создание курсора для навигации по БД

    if is_included(username):   # проверка наличия пользователя в БД
        return 'Пользователь с таким именем уже существует!'

    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'{username}', f'{email}', f'{age}', '1000'))   # добавление пользователя в БД

    connection.commit()     # сохранение изменений
    connection.close()      # закрытие соединения

    return 'Пользователь успешно добавлен!'



def get_all_products():
    connection = sqlite3.connect('database.db')     # подключение к БД
    cursor = connection.cursor()    # создание курсора для навигации по БД

    cursor.execute('SELECT * FROM Products')    # запрос всех записей в таблице Products
    products = cursor.fetchall()    # сохранение полученных данных в переменную

    connection.close()      # закрытие соединения
    return products     # возвращаем результат запроса

def initial_data():
    connection = sqlite3.connect('database.db')     # подключение к БД
    cursor = connection.cursor()    # создание курсора для навигации по БД

    for i in range(1, 5):   # генерируем данные для наполнения БД
        cursor.execute('SELECT title FROM Products WHERE title=?', (f'Продукт {i}',))    # запрос наличия записи в БД
        if cursor.fetchone() is None:   # если запись отсутствует
            cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                           (f'Продукт {i}', f'Описание {i}', f'{i * 100}')) # добавляем запись в БД

    connection.commit()     # сохранение изменений
    connection.close()      # закрытие соединения
