import mysql.connector

# Подключение к базе данных
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="MyDB"
)

cursor = mydb.cursor()

def list_tables():
    # Функция для вывода имен доступных таблиц
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Доступные таблицы:")
    for table in tables:
        print(table[0])

def choose_table():
    table_name = input("Введите имя таблицы: ")
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    existing_tables = cursor.fetchall()
    if existing_tables:
        return table_name
    else:
        print(f"Таблица с именем '{table_name}' не существует. Пожалуйста, введите правильное имя таблицы.")
        choose_table()

def get_table_fields(table_name):
    # Функция для получения информации о полях таблицы
    query = f"DESCRIBE {table_name}"
    cursor.execute(query)
    fields = [row[0] for row in cursor.fetchall()]
    return fields

def get_auto_increment_field(table_name):
    # Функция для определения автоинкрементного поля (id)
    query = f"SHOW COLUMNS FROM {table_name} WHERE Extra = 'auto_increment'"
    cursor.execute(query)
    auto_increment_field = cursor.fetchone()
    return auto_increment_field[0] if auto_increment_field else None

def get_foreign_key_fields(table_name):
    # Функция для получения полей, являющихся внешними ключами
    query = f"SELECT COLUMN_NAME, REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table_name}' AND CONSTRAINT_NAME != 'PRIMARY'"
    cursor.execute(query)
    foreign_key_fields = cursor.fetchall()
    return foreign_key_fields

def get_foreign_table_data(foreign_table, foreign_table_fields):
    # Функция для получения данных из другой таблицы для выбора необходимых полей
    query = f"SELECT {', '.join(foreign_table_fields)} FROM {foreign_table}"
    cursor.execute(query)
    foreign_table_data = cursor.fetchall()
    return foreign_table_data

def insert_data(table_name):
    # Функция для ввода данных в таблицу
    fields = get_table_fields(table_name)
    auto_increment_field = get_auto_increment_field(table_name)
    foreign_key_fields = get_foreign_key_fields(table_name)
    data = {}
    if auto_increment_field in fields:
        fields.remove(auto_increment_field)

    print(f"Введите данные для таблицы {table_name}:")
    for field in fields:
        if field == 'date_of_purchase' or field == 'date_of_last_delivery':
            continue

        if field == 'amount':
            if table_name == 'cart':
                drug_id = data['drug_id']
                quantity = data['quantity']
                cursor.execute(f'SELECT `price` FROM `warehouse` WHERE `drug_id` = {drug_id}')
                price = cursor.fetchone()[0]
                result = int(price) * int(quantity)
                data['amount'] = result
                continue
            if table_name == 'purchase':
                buyer_id = data['buyer_id']
                cursor.execute(f'SELECT `amount` FROM `cart` WHERE `buyer_id` = {buyer_id}')
                items_in_cart = cursor.fetchall()
                data['amount'] = sum(int(item[0]) for item in items_in_cart) if items_in_cart else 0
                continue

        if field in [item[0] for item in foreign_key_fields]:
            foreign_table = [item[1] for item in foreign_key_fields if item[0] == field][0]
            foreign_table_fields = get_table_fields(foreign_table)
            print(f"Доступные данные для поля {field}:")
            foreign_table_data = get_foreign_table_data(foreign_table, foreign_table_fields)
            for i, row in enumerate(foreign_table_data):
                print(f"{i + 1}. {row[1]}")
            while True:
                values = input(f"Введите номер записи для {field}: ")
                if values.isdigit() and 1 <= int(values) <= len(foreign_table_data):
                    data[field] = int(values)
                    break
                print("Некорректный выбор. Попробуйте еще раз.")
        else:
            value = input(f"{field}: ")
            data[field] = value

    if auto_increment_field in data:
        data.pop(auto_increment_field)

    if foreign_key_fields:
        for field, value in data.items():
            if field in [item[0] for item in foreign_key_fields]:
                foreign_table = [item[1] for item in foreign_key_fields if item[0] == field][0]
                foreign_table_fields = get_table_fields(foreign_table)
                data[field] = get_foreign_table_data(foreign_table, foreign_table_fields)[value - 1][0]

    for field in fields:
        if field not in data:
            data[field] = None

    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({placeholders})"
    cursor.execute(query, list(data.values()))
    mydb.commit()
    print("Data successfully added.")


def print_table_data(table_name):
    # Получаем названия полей таблицы
    fields = get_table_fields(table_name)
    # Получаем название поля с автоинкрементом
    auto_increment_field = get_auto_increment_field(table_name)
    # Удаляем поле с автоинкрементом из списка полей
    fields.remove(auto_increment_field)
    # Получаем название полей с внешними ключами
    foreign_key_fields = get_foreign_key_fields(table_name)

    # Выводим шапку таблицы
    header = '|'.join(fields)
    print(header)

    # Формируем запрос на выборку данных из таблицы
    query = f"SELECT {', '.join(fields)} FROM {table_name}"
    cursor.execute(query)
    # Получаем все строки таблицы
    table_data = cursor.fetchall()

    # Определяем максимальную длину значений для каждого столбца
    max_lengths = [max(len(str(value)) for value in column) for column in zip(*table_data)]

    # Выводим данные таблицы с красивым форматированием
    for row in table_data:
        formatted_row = []
        for field, value, length in zip(fields, row, max_lengths):
            if field in [item[0] for item in foreign_key_fields]:
                # Если поле является внешним ключом, то заменяем его значение
                # на соответствующее значение из связанной таблицы
                foreign_table = [item[1] for item in foreign_key_fields if item[0] == field][0]
                foreign_table_fields = get_table_fields(foreign_table)
                foreign_table_data = get_foreign_table_data(foreign_table, foreign_table_fields)
                related_value = next((row[1] for row in foreign_table_data if row[0] == value), value)
                formatted_row.append(str(related_value).ljust(length))
            else:
                # Если поле не является внешним ключом, то просто добавляем его значение
                formatted_row.append(str(value).ljust(length))

        print('|'.join(formatted_row))

list_tables()
table_name = choose_table()

while True:
    print("1. Получение информации о полях таблицы")
    print("2. Вывод записей")
    print("3. Ввод данных в таблицу")
    print("4. Выбор другой таблицы")
    print("5. Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        fields = get_table_fields(table_name)
        print("Поля таблицы:", fields)
    elif choice == "2":
        print_table_data(table_name)
    elif choice == "3":
        insert_data(table_name)
    elif choice == "4":
        table_name = choose_table()
    elif choice == "5":
        break
    else:
        print("Неверный выбор. Попробуйте снова.")

# Закрытие соединения
cursor.close()
mydb.close()