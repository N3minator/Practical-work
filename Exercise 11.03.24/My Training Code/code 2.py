import sqlite3
import bcrypt

# Подключение к базе данных (или создание, если она не существует)
conn = sqlite3.connect('users.db')
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
        conn.commit()
        print("Регистрация прошла успешно!")
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким логином уже существует.")

def login():
    """Авторизует пользователя."""
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    cursor.execute("SELECT password_hash, admin FROM users WHERE login=?", (login,))
    # Получаем хэш пароля и статус администратора
    result = cursor.fetchone()
    if result and check_password(result[0], password):
        if result[1] == 'True':
            print("Вход выполнен успешно! Вы администратор.")
        else:
            print("Вход выполнен успешно! Вы не администратор.")
    else:
        print("Неверный логин или пароль.")


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