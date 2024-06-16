import mysql.connector

# Подключение к серверу MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = conn.cursor()

# Создание базы данных myDB, если она не существует
cursor.execute("CREATE DATABASE IF NOT EXISTS myDB")
cursor.execute("USE myDB")

# Чтение SQL-файла с учетом кодировки UTF-8
with open("create_tables_MySQL.sql", "r", encoding="utf-8") as file:
    sql_statements = file.read().split(';')
    for sql in sql_statements:
        if sql.strip():  # Игнорируем пустые строки
            cursor.execute(sql)

conn.commit()

# Закрытие соединения
cursor.close()
conn.close()

print("Таблицы успешно созданы.")