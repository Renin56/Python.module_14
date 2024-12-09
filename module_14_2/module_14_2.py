import sqlite3


connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
        )
    ''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', f'{i * 10}', '1000'))

for i in range(1, 11):
    cursor.execute('UPDATE Users SET balance = ? WHERE id % 2 == 1', (500,))

for i in range(1, 11):
    cursor.execute('DELETE FROM Users WHERE id % 3 == 1')

cursor.execute('SELECT * FROM Users WHERE age != ?', (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

print('*' * 50)

# удаляем запись с id = 6
cursor.execute('DELETE FROM Users WHERE id == 6')

# узнаем общее кол-во записей
cursor.execute('SELECT COUNT(*) FROM Users')
print(f'Всего записей: {cursor.fetchone()[0]}')

# узнаем общий баланс
cursor.execute('SELECT SUM(balance) FROM Users')
print(f'Общий баланс: {cursor.fetchone()[0]}')

# узнаем среднее значение баланса
cursor.execute('SELECT AVG(balance) FROM Users')
print(f'Средний баланс: {cursor.fetchone()[0]}')

connection.commit()
connection.close()
