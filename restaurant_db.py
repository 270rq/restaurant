import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Создаем таблицу пользователей (users)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT,
                    status TEXT
                )''')

# Создаем таблицу заказов (orders)
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_number INTEGER,
                    count INTEGER,
                    items TEXT,
                    status TEXT,
                    supervisor_id INTEGER,
                    FOREIGN KEY (supervisor_id) REFERENCES users(id)

                )''')

# Создаем таблицу смен (shift)
cursor.execute('''CREATE TABLE IF NOT EXISTS shift (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supervisor_id INTEGER,
                    FOREIGN KEY (supervisor_id) REFERENCES users(id)
                )''')

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()