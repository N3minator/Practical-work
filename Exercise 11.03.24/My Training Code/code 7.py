import sqlite3
import bcrypt
import random
from datetime import datetime, timedelta

def hash_password(password):
    """Хеширует пароль с помощью bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(stored_password, provided_password):
    """Проверяет пароль с хешем."""
    return bcrypt.checkpw(provided_password.encode(), stored_password)


def create_tables():
    """Создает таблицы в базе данных."""
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                          (id_books INTEGER PRIMARY KEY, name_books TEXT, author TEXT, genre TEXT, visible BOOLEAN)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id_users INTEGER PRIMARY KEY, login TEXT, password TEXT, password_hash TEXT, gmail TEXT, admin TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_books
                          (id_users INTEGER,
                           login TEXT,
                           id_books INTEGER,
                           date_rented TIMESTAMP, 
                           return_date TIMESTAMP,
                           FOREIGN KEY (id_users) REFERENCES users(id_users),
                           FOREIGN KEY (id_books) REFERENCES books(id_books))''')
        conn.commit()
        main(cursor, conn)


def register(cursor, conn):
    """Регистрирует нового пользователя."""
    login = input("\nВведите логин: ")
    password = input("Введите пароль: ")
    gmail = input("Введите Gmail: ")
    user_id_str = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    user_id = int(user_id_str)
    del user_id_str

    while True:
        print('Вы хотите стать Админом?')
        choice_admin = input("Ваш выбор y/n:").lower().strip()
        if choice_admin in ['y', 'n']:
            admin = 'True' if choice_admin == 'y' else 'False'
            break
        else:
            print('Неверная команда!')

    password_hash = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (id_users, login, password, password_hash, gmail, admin) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, login, password, password_hash, gmail, admin))
        conn.commit()
        print("\nРегистрация прошла успешно!")

        books(login, cursor, conn, user_id)
    except sqlite3.IntegrityError:
        print("\nОшибка: Пользователь с таким логином уже существует.")


def login(cursor, conn):
    """Авторизует пользователя."""
    login = input("\nВведите логин: ")
    password = input("Введите пароль: ")

    cursor.execute("SELECT id_users, password_hash, admin FROM users WHERE login=?", (login,))
    result = cursor.fetchone()
    if result and check_password(result[1], password):
        print(f"\nВход выполнен успешно! Статус админа: {result[2]}")

        # В result мы передаем id пользователя
        books(login, cursor, conn, result[0])
    else:
        print("\nНеверный логин или пароль.")


def books(login, cursor, conn, user_id=None):
    """Меню действий с книгами."""
    while True:
        print('''\nЧто вы хотите сделать?
        1. Посмотреть доступные книги
        2. Посмотреть взятые книги пользователями (Админ)
        3. Взять на прокат
        4. Вернуть книгу
        5. Посмотреть ваш список взятых книг
        6. Добавить книгу (Админ)
        7. Удалить книгу (Админ)
        0. Выйти
        ''')
        action = input('Выберите действие: ')
        print()
        if action == "1":
            # Открываем базу данных с доступными книгами
            cursor.execute("SELECT * FROM books WHERE visible=1")
            # Отображаем доступные книги из базы данных
            for book in cursor.fetchall():
                print(f"Номер книги: {book[0]}, Название книги: {book[1]}, Автор: {book[2]}, Жанр: {book[3]}")
        elif action == '2':
            cursor.execute("SELECT admin FROM users WHERE login=?", (login,))
            if cursor.fetchone()[0] == 'True':
                list_rented_books(cursor)
            else:
                print('Отказано в доступе! Вы не Админ!')
        elif action == '3':
            buy_book(conn, cursor, login, user_id)

        elif action in ["6", "7"]:
            cursor.execute("SELECT admin FROM users WHERE login=?", (login,))
            # if cursor.fetchone()[0] == 'True || Проверяет является ли пользователей Админом
            if cursor.fetchone()[0] == 'True':
                if action == "6":
                    add_book(conn, cursor)
                else:
                    del_book(conn, cursor)
            else:
                print("Отказано в доступе! Вы не Админ!")

        elif action == "0":
            break
        else:
            print("Неверная команда.")
            continue  # Возвращаемся к началу цикла для ввода новой команды


def buy_book(conn, cursor, login, user_id):
    """Позволяет пользователю взять книгу на прокат."""
    cursor.execute("SELECT * FROM books WHERE visible=1")
    for book in cursor.fetchall():
        print(f"Номер книги: {book[0]}, Название книги: {book[1]}, Автор: {book[2]}, Жанр: {book[3]}")

    book_id = int(input('\nВыберите пожалуйста номер книги: '))

    # Проверяем, существует ли книга с таким ID, независимо от её статуса (взята или доступна).
    cursor.execute("SELECT visible FROM books WHERE id_books=?", (book_id,))
    book_info = cursor.fetchone()

    # Если книга существует в базе данных
    if book_info:
        is_book_available = book_info[0]

        if is_book_available:
            cursor.execute("UPDATE books SET visible=0 WHERE id_books=?", (book_id,))
            date_rented = datetime.now().strftime("%d/%m/%Y")
            return_date = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")  # Добавляем 7 дней к дате взятия книги на прокат

            cursor.execute(
                "INSERT INTO user_books (id_users, login, id_books, date_rented, return_date) VALUES (?, ?, ?, ?, ?)",
                (user_id, login, book_id, date_rented, return_date))
            conn.commit()
            print(f"\nКнига успешно взята на прокат до {return_date}.")
        else:
            print('\nДанная книга уже взята!')
    else:
        print('\nНеверный ввод ID книги')


def list_rented_books(cursor):
    """Отображает список взятых книг."""
    cursor.execute("""SELECT b.id_books, b.name_books, b.author, b.genre, ub.date_rented, ub.return_date, u.login, u.id_users
                      FROM user_books ub
                      JOIN books b ON ub.id_books = b.id_books
                      JOIN users u ON ub.id_users = u.id_users""")
    print("Книги, взятые на прокат:")
    for row in cursor.fetchall():
        print(f"ID Книги: {row[0]} | Название: {row[1]} | Автор: {row[2]} | Жанр: {row[3]} | Взято: {row[4]} | До: {row[5]} | Пользователь: {row[6]} | ID пользователя: {row[7]}")


def add_book(conn, cursor):
    """Добавляет новую книгу в каталог."""
    name_books = input('Введите название книги: ')
    author = input('Введите автора книги: ')
    genre = input('Введите жанр книги: ')
    visible = input('Книга доступна для проката? (1 - да, 0 - нет): ')

    cursor.execute("INSERT INTO books (name_books, author, genre, visible) VALUES (?, ?, ?, ?)",
                   (name_books, author, genre, visible))
    conn.commit()
    print("Книга успешно добавлена.")


def del_book(conn, cursor):
    """Удаляет книгу из каталога."""
    book_id = input("Введите ID книги для удаления: ")

    # Открываем базу данных для поиска информации
    cursor.execute("SELECT COUNT(*) FROM books WHERE id_books=?", (book_id,))

    # Проверяет, существует ли книга с заданным названием.
    if cursor.fetchone()[0]:
        cursor.execute("DELETE FROM books WHERE id_books=?", (book_id,))
        conn.commit()
        print("\nКнига успешно удалена!")
    else:
        print('\nКнига с заданным ID не найдена!')


def main(cursor, conn):
    """Основное меню приложения."""
    while True:
        action = input("Выберите действие: регистрация или вход (reg/log): ")
        if action == "reg":
            register(cursor, conn)
        elif action == "log":
            login(cursor, conn)
        else:
            print("Неверная команда.")

        while True:
            continue_ = input("Продолжить? (y/n): ").lower().strip()
            if continue_ == "y":
                print()
                break
            elif continue_ == "n":
                print()
                return
            else:
                print("Неверная команда!")


if __name__ == "__main__":
    create_tables()
