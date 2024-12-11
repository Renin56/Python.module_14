import sqlite3


def initial_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL    
        )
        ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products

def initial_data():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    for i in range(1, 5):
        cursor.execute('SELECT title FROM Products WHERE title=?', (f'Продукт{i}',))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                           (f'Продукт{i}', f'Описание{i}', f'{i * 100}'))

    connection.commit()
    connection.close()