import sqlite3
import bcrypt

# Coединение с базой данных будет автоматически закрыто после завершения блока кода.
with sqlite3.connect('users.db') as conn:
    # После создания курсора вы можете вызывать методы для выполнения запросов к базе данных, такие как execute(), fetchone(), fetchall() и другие, используя этот курсор.
    cursor = conn.cursor()

    # Создание таблицы пользователей, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (login TEXT PRIMARY KEY, password TEXT, password_hash TEXT, gmail TEXT, admin TEXT)''')


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
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    gmail = input("Введите Gmail: ")

    while True:
        print('Вы хотите стать Админом?')

        choice_admin = input("Ваш выбор да/нет:").lower()

        if choice_admin == 'да':
            admin = 'True'
            break
        elif choice_admin == 'нет':
            admin = 'False'
            break
        else:
            print("Неверная команда!")

    # Хеширование пароля
    password_hash = hash_password(password)

    # Если в блоке try происходит ошибка, интерпретатор Python прекращает выполнение кода в блоке try и переходит к соответствующему блоку except, который соответствует этому типу ошибки.
    # Это позволяет программе продолжить выполнение, минуя ошибку или выполнить дополнительные действия, связанные с обработкой ошибки.
    try:
        cursor.execute("INSERT INTO users (login, password, password_hash, gmail, admin) VALUES (?, ?, ?, ?, ?)", (login, password, password_hash, gmail, admin))

        # Через conn.commit() подтверждаем изменения в базе данных
        conn.commit()

        print("Регистрация прошла успешно!")
        books(login, conn, cursor)  # Передача соединения и курсора
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким логином уже существует.")


def login():
    """Авторизует пользователя."""
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash, admin FROM users WHERE login=?", (login,))
        # Получаем хэш пароля и статус администратора
        result = cursor.fetchone()
        if result and check_password(result[0], password):
            print(f"Вход выполнен успешно! Статус админа: {result[1]}")
            books(login, conn, cursor)  # Передача соединения и курсора
        else:
            print("Неверный логин или пароль.")


def books(login, conn, cursor):
    # Создание таблицы книг, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                       (id_books INTEGER PRIMARY KEY, name_books TEXT, author TEXT, genre TEXT)''')

    while True:
        print('Что вы хотите сделать?')
        action = input('Выберите действие: посмотреть книги/добавить книги/удалить книги/выйти (see/add/del/exit): ')
        if action == "see":
            see_books(login, conn, cursor)
        elif action == "add":
            # Проверяем статус админа
            cursor.execute("SELECT admin FROM users WHERE login=?", (login,))
            result = cursor.fetchone()
            if result and result[0] == 'True':
                print(f"Доступ разрешен! Статус админа {result[0]}")
                add_book(conn, cursor)
            else:
                print("Отказано в доступе! Вы не Админ!")
        elif action == "del":
            # Проверяем статус админа
            cursor.execute("SELECT admin FROM users WHERE login=?", (login,))
            result = cursor.fetchone()
            if result and result[0] == 'True':
                print(f"Доступ разрешен! Статус админа {result[0]}")
                del_book(conn, cursor)
            else:
                print("Отказано в доступе! Вы не Админ!")
        elif action == "exit":
            break
        else:
            print("Неверная команда.")
            continue  # Возвращаемся к началу цикла для ввода новой команды


def add_book(conn, cursor):
    # Получаем максимальное значение id_books из таблицы books
    cursor.execute("SELECT MAX(id_books) FROM books")
    max_id_books = cursor.fetchone()[0]
    new_id_books = max_id_books + 1 if max_id_books is not None else 1  # Увеличиваем максимальное значение на 1 или начинаем с 1, если таблица пуста

    name_books = input('Введите название книги:')
    author = input('Введите автора книги:')
    genre = input('Введите жанр книги:')

    # Вставляем новую запись с новым значением id_books
    cursor.execute("INSERT INTO books (id_books, name_books, author, genre) VALUES (?, ?, ?, ?)",
                   (new_id_books, name_books, author, genre))
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


def see_books(login, conn, cursor):

    print() # Добавляем пустую строку для разделения книг

    # Выполняем запрос, чтобы получить все записи из таблицы books
    cursor.execute("SELECT * FROM books")

    # Извлекаем все строки (записи) из результата запроса
    books_data = cursor.fetchall()

    # Выводим каждую запись в консоль
    for book in books_data:
        print("Номер книги:", book[0]),
        print("Название книги:", book[1])
        print("Автор:", book[2])
        print("Жанр:", book[3])
        print()  # Добавляем пустую строку для разделения книг

    books(login, conn, cursor)


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
                break
            elif continue_ == "нет":
                return
            else:
                print("Неверная команда!")


if __name__ == "__main__":
    main()