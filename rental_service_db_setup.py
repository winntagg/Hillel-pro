import sqlite3


def create_db_and_tables():
    conn = sqlite3.connect('rental_service.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tax_ids (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            tax_id TEXT NOT NULL UNIQUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rental_contracts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            contract_number TEXT NOT NULL UNIQUE,
            item TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS past_rental_contracts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            contract_number TEXT NOT NULL UNIQUE,
            item TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    return conn, cursor


def add_data(cursor):
    # Данные о пользователях
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")

    # Налоговые номера
    cursor.execute("INSERT INTO tax_ids (user_id, tax_id) VALUES (1, 'TAX123456')")
    cursor.execute("INSERT INTO tax_ids (user_id, tax_id) VALUES (2, 'TAX789101')")
    cursor.execute("INSERT INTO tax_ids (user_id, tax_id) VALUES (3, 'TAX112131')")

    # Текущие контракты аренды
    cursor.execute(
        "INSERT INTO rental_contracts (user_id, contract_number, item, start_date, end_date) VALUES (1, 'CONTRACT001', 'Apartment', '2023-01-01', '2023-12-31')")
    cursor.execute(
        "INSERT INTO rental_contracts (user_id, contract_number, item, start_date, end_date) VALUES (2, 'CONTRACT002', 'Car', '2023-02-01', '2023-08-01')")
    cursor.execute(
        "INSERT INTO rental_contracts (user_id, contract_number, item, start_date, end_date) VALUES (3, 'CONTRACT003', 'Bike', '2023-03-01', '2023-09-01')")

    # Прошлые контракты аренды
    cursor.execute(
        "INSERT INTO past_rental_contracts (user_id, contract_number, item, start_date, end_date) VALUES (1, 'CONTRACT_PREV001', 'House', '2022-01-01', '2022-12-31')")
    cursor.execute(
        "INSERT INTO past_rental_contracts (user_id, contract_number, item, start_date, end_date) VALUES (2, 'CONTRACT_PREV002', 'Scooter', '2022-02-01', '2022-08-01')")
    cursor.execute(
        "INSERT INTO past_rental_contracts (user_id, contract_number, item, start_date, end_date) VALUES (3, 'CONTRACT_PREV003', 'Office', '2022-03-01', '2022-09-01')")

    conn.commit()


def execute_queries(cursor):
    # SELECT запит - отримання всіх користувачів
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        print(user)

    # INSERT запит - додавання нового користувача
    cursor.execute("INSERT INTO users (name, email) VALUES ('Dave', 'dave@example.com')")
    conn.commit()

    # UPDATE запит - зміна даних користувача
    cursor.execute("UPDATE users SET email = 'alice_new@example.com' WHERE name = 'Alice'")
    conn.commit()

    # JOIN запит - отримання інформації про контракти разом з іменами користувачів
    cursor.execute('''
        SELECT users.name, rental_contracts.contract_number, rental_contracts.item
        FROM users
        JOIN rental_contracts ON users.id = rental_contracts.user_id
    ''')
    results = cursor.fetchall()
    print("\nJoined Data (users and rental contracts):")
    for result in results:
        print(result)


if __name__ == '__main__':
    conn, cursor = create_db_and_tables()
    add_data(cursor)
    execute_queries(cursor)
    conn.close()