import sqlite3
import bcrypt


def hash_password(password):
    """Хеширует пароль с помощью bcrypt."""
    # password.encode() || переменную password превращает из str в bite
    # bcrypt.gensalt() || Генерирует Соль которая усиливает защиту от атак
    # Хешируем пароль
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(stored_password, provided_password):
    """Проверяет пароль с хешем."""
    # stored_password, который представляет собой хэшированный пароль, хранящийся в базе данных
    # provided_password, который представляет введенный пользователем пароль для проверки.
    # Он принимает два аргумента: предоставленный пароль, который сначала кодируется в байты с помощью encode(), и сохраненный хэш пароля из базы данных.
    # Функция затем сравнивает хэши и возвращает True, если они совпадают, и False в противном случае.
    return bcrypt.checkpw(provided_password.encode(), stored_password)


def register():
    """Регистрирует нового пользователя."""
    login = input("\nВведите логин: ")
    password = input("Введите пароль: ")
    gmail = input("Введите Gmail: ")

    while True:
        print('Вы хотите стать Админом?')

        choice_admin = input("Ваш выбор да/нет:").lower()

        if choice_admin in ['да', 'нет']:
            admin = 'True' if choice_admin == 'да' else 'False'
            break
        else:
            print('Неверная команда!')

    # Хеширование пароля
    password_hash = hash_password(password)

    # Если в блоке try происходит ошибка, интерпретатор Python прекращает выполнение кода в блоке try и переходит к соответствующему блоку except, который соответствует этому типу ошибки.
    # Это позволяет программе продолжить выполнение, минуя ошибку или выполнить дополнительные действия, связанные с обработкой ошибки.
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            # Создаем базу данных пользователей если она не существует
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                           (login TEXT PRIMARY KEY, password TEXT, password_hash TEXT, gmail TEXT, admin TEXT)''')

            cursor.execute("INSERT INTO users (login, password, password_hash, gmail, admin) VALUES (?, ?, ?, ?, ?)",
                           (login, password, password_hash, gmail, admin))
            # Через conn.commit() подтверждаем изменения в базе данных
            conn.commit()

        print("\nРегистрация прошла успешно!")
        books(login)  # Передача соединения и курсора
    except sqlite3.IntegrityError:
        print("\nОшибка: Пользователь с таким логином уже существует.")


def login():
    """Авторизует пользователя."""
    login = input("\nВведите логин: ")
    password = input("Введите пароль: ")

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash, admin FROM users WHERE login=?", (login,))
        # Получаем хэш пароля и статус администратора
        result = cursor.fetchone()
        if result and check_password(result[0], password):
            print(f"\nВход выполнен успешно! Статус админа: {result[1]}")
            books(login)  # Передача соединения и курсора
        else:
            print("\nНеверный логин или пароль.")


def books(login):
    # Создание таблицы книг, если она еще не существует
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                          (id_books INTEGER PRIMARY KEY, name_books TEXT, author TEXT, genre TEXT, visible BOOLEAN)''')
        while True:
            print('''\nЧто вы хотите сделать?

            1.Посмотреть доступные книги
            2.Посмотреть недоступные книги (Админ)
            3.Взять на прокат
            4.Вернуть книгу
            5.Посмотреть ваш список взятых книг
            6.Добавить книги (Админ)
            7.Удалить книги (Админ)
            0.Выйти
            ''')
            action = input('Выберите действие: ')
            print()
            if action == "1":
                # Выполняем запрос, чтобы получить все записи из таблицы books, где visible == True (1)
                cursor.execute("SELECT * FROM books WHERE visible=1")
                for book in cursor.fetchall():
                    print(f"Номер книги: {book[0]}, | Название книги: {book[1]}, | Автор: {book[2]}, | Жанр: {book[3]}")

            elif action == '2':
                # Выполняем запрос, чтобы получить все записи из таблицы books, где visible == True (1)
                cursor.execute("SELECT * FROM books WHERE visible=0")
                for book in cursor.fetchall():
                    print(f'Номер книги: {book[0]}, | Название книги: {book[1]}, | Автор: {book[2]}, | Жанр: {book[3]}')

            elif action == '3':
                buy_book(conn, cursor)

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

def buy_book(conn, cursor):
    print('Какую книгу вы хотите взять?\n')
    # Выполняем запрос, чтобы получить все записи из таблицы books, где visible == True (1)
    cursor.execute("SELECT * FROM books WHERE visible=1")

    for book in cursor.fetchall():
        print(f"Номер книги: {book[0]}, | Название книги: {book[1]}, | Автор: {book[2]}, | Жанр: {book[3]}")

    book_id = int(input('Выберите пожалуйста номер книги: '))

    # Проверяем, существует ли книга с таким id_books и что она доступна
    cursor.execute("SELECT * FROM books WHERE id_books=? AND visible=1", (book_id,))
    # В переменную book_info записываем всю информацию о выбранной книге пользователем
    book_info = cursor.fetchone()

    if book_info:
        # Обновляем видимость книги на 0 (недоступно), поскольку книга взята на прокат
        cursor.execute("UPDATE books SET visible=0 WHERE id_books=?", (book_id,))
        # Через conn.commit() подтверждаем изменения в базе данных
        conn.commit()
        print(f"Книга '{book_info[1]}' успешно взята на прокат!")
    else:
        print(f"Книга с указанным номером {book_id} не найдена или уже взята.")

def add_book(conn, cursor):
    # Получаем максимальное значение id_books из таблицы books
    cursor.execute("SELECT MAX(id_books) FROM books")
    max_id_books = cursor.fetchone()[0]
    # Увеличиваем максимальное значение на 1 или начинаем с 1, если таблица пуста
    new_id_books = max_id_books + 1 if max_id_books is not None else 1

    name_books = input('Введите название книги:')
    author = input('Введите автора книги:')
    genre = input('Введите жанр книги:')
    visible = 1

    # Вставляем новую запись с новым значением id_books
    cursor.execute("INSERT INTO books (id_books, name_books, author, genre, visible) VALUES (?, ?, ?, ?, ?)",
                   (new_id_books, name_books, author, genre, visible))
    # Через conn.commit() подтверждаем изменения в базе данных
    conn.commit()


def del_book(conn, cursor):
    try:
        book_id = int(input("Введите номер книги для удаления: "))
        cursor.execute("DELETE FROM books WHERE id_books=?", (book_id,))

        # Через conn.commit() подтверждаем изменения в базе данных
        conn.commit()

        print("Книга успешно удалена.")
    except ValueError:
        print("Неверный формат номера книги.")
    except sqlite3.Error as e:
        print("Ошибка удаления книги:", e)


def main():
    while True:
        action = input("Выберите действие: регистрация или вход (reg/log): ")
        if action == "reg":
            register()
        elif action == "log":
            login()
        else:
            print("Неверная команда.")

        while True:
            continue_ = input("Продолжить? (да/нет): ").lower()
            if continue_ == "да":
                print()
                break
            elif continue_ == "нет":
                print()
                return
            else:
                print("Неверная команда!")


if __name__ == "__main__":
    main()