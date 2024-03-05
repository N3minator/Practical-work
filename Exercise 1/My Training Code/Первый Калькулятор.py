# Проект который имеет функционал:
# 1. Создание/вход в акаунт
# 2. Аккаунты обычных пользователей и администраторов
# 3. Простой калькулятор
# 4. Сделать куча проверок на любых действиях, чтобы программа выдавала меньше ошибок и не только...

# Добавить функцию забыл пароль. Где пользователь вводит свой gmail и ID который в приватном доступе был виден только ему. И через ID он сбрасывает пароль от акаунта
# Сделать акаунт администратора, который может, просматривать все акаунты и удалять акаунты
# Исправить ошибку когда создаёшь новый акаунт а потом выходишь из него и пытаешься войти в него то выдаёт ошибку

import random
from cryptography.fernet import Fernet

# Генерация ключа для шифрования пароля
password_key = Fernet.generate_key()
password_cipher_suite = Fernet(password_key)

# Генерация ключа для шифрования ID
id_key = Fernet.generate_key()
id_cipher_suite = Fernet(id_key)

# Словарь для хранения информации об аккаунтах
accounts = {
    'bogotur4ik@gmail.com': {
        'name': 'BogoTur4ik',
        'password': 'vitaha',
        'ID': 123456789,
        'admin': True
    }
}

def create_account():
    print("\nСистема создания аккаунта!\n")
    name = input('Придумайте никнейм -> ').strip()
    gmail = input('Введите свой gmail -> ').strip().lower()

    # Проверяем, содержит ли gmail доменную часть "@gmail.com"
    if not gmail.endswith("@gmail.com"):
        gmail += "@gmail.com"

    while True:
        password1 = input('Создайте пароль -> ').strip()
        password2 = input('Повторите пароль -> ').strip()

        if password1 != password2:
            print('\nПароли не совпадают! Попробуйте снова...\n')
        else:
            # Шифруем пароль перед сохранением
            encrypted_password = password_cipher_suite.encrypt(password1.encode())
            del password1, password2
            break

    # Генерирует случайный ID пользователя
    id_user = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    id_user = int(id_user)

    users = {'Name': name, 'Gmail': gmail, 'Password': encrypted_password, 'ID': id_user}

    accounts[gmail] = users

    print(f"\nВы успешно создали аккаунт!\n")
    print(f"Ваш ID: {id_user}\n")

    show_menu(gmail)


def login():
    print("\nСистема входа в аккаунт!\n")
    gmail = input('Введите свой gmail -> ').strip().lower()

    # Проверяем, содержит ли gmail доменную часть "@gmail.com"
    if not gmail.endswith("@gmail.com"):
        gmail += "@gmail.com"

    password = input('Введите пароль -> ').strip()

    if gmail in accounts:
        if accounts[gmail]['password'] == password:
            print(f"\nВы вошли в акаунт {accounts[gmail]['name']}\n")
            show_menu(gmail)
        else:
            print("\nНеправильный пароль!")
    else:
        print("\nАккаунт с таким gmail не найден!")


# Тут проблемы с ID который не хочет проверяться
def recovery_account():
    gmail = input('Введите свой gmail -> ').strip().lower()

    # Проверяем, содержит ли gmail доменную часть "@gmail.com"
    if not gmail.endswith("@gmail.com"):
        gmail += "@gmail.com"

    ID = input('Введите ваш ID -> ').strip()

    if gmail in accounts:
        if accounts[gmail]['ID'] == ID:
            while True:
                password1 = input('Введите новый пароль -> ').strip()
                password2 = input('Повторите пароль -> ').strip()

                if password1 != password2:
                    print('\nПароли не совпадают! Попробуйте снова...\n')
                else:
                    break
            # После окончания смены пароля, мы переходим в меню пользователя
            show_menu(gmail)
        else:
            print("\nНеправильный ID!")
    else:
        print("\nАккаунт с таким gmail не найден!")


def show_menu(gmail):
    print("Меню выбора:")
    print("1. Запустить калькулятор")
    # if accounts[gmail]['Admin']:
    # print("3. Просмотреть список всех аккаунтов")
    # print("4. Удалить аккаунт")
    print("0. Выход из программы")

    while True:
        choice = input('\nВаш выбор -> ').strip()

        if choice == '1':
            manual_calculator(gmail)
        elif choice == '2' and accounts[gmail]['Admin']:
            show_all_accounts()
        elif choice == '3' and accounts[gmail]['Admin']:
            delete_account()
        elif choice == '0':
            break
        else:
            print("Неправильный выбор!")


def manual_calculator(gmail):
    print("\nДобро пожаловать в калькулятор!\n")

    while True:
        num_1 = int(input('Напишите первое число -> '))
        num_2 = int(input('Напишите второе число -> '))

        operation = input('Выберите операцию (+, -, /, *) -> ')

        if operation == '+':
            print(f'Результат: {num_1} + {num_2} = {num_1 + num_2}')

        elif operation == '-':
            print(f'Результат: {num_1} - {num_2} = {num_1 - num_2}')

        elif operation == '/':
            if num_2 == 0:
                print('Ошибка! Деление на ноль!')
            else:
                print(f'\nРезультат: {num_1} / {num_2} = {num_1 / num_2}')
        elif operation == '*':
            print(f'\nРезультат: {num_1} * {num_2} = {num_1 * num_2}')
        else:
            print('\nНеправильная операция!')

        choice = input('\nЖелаете выйти? да/нет -> ').strip().lower()

        if choice == 'да':
            break
    show_menu(gmail)


def show_all_accounts():
    print("\nСписок всех аккаунтов:")
    for gmail, user_info in accounts.items():
        print(f"Gmail: {gmail}, Имя: {user_info['Name']}, ID: {user_info['ID']}")


def delete_account():
    gmail = input('Введите gmail аккаунта, который хотите удалить -> ').strip().lower()

    if gmail in accounts:
        del accounts[gmail]
        print(f"Аккаунт с gmail {gmail} успешно удален!")
    else:
        print("\nАккаунт с таким gmail не найден!")


def main():
    print("Добро пожаловать!")

    while True:
        print("\nВыберите действие:")
        print("1. Создать новый аккаунт")
        print("2. Войти в существующий аккаунт")
        print("3. Восстановление аккаунта")
        print("0. Выход из программы")

        choice = input(f'\nВаш выбор -> ').strip()

        if choice == '1':
            # Запускаем функцию создания акаунта
            create_account()
        elif choice == '2':
            # Запускаем функцию вход в акаунт
            login()
        elif choice == '3':
            recovery_account()
        elif choice == '0':
            # Выход из программы
            break
        else:
            print("\nНеправильный выбор!")


# Активируем функцию main
if __name__ == "__main__":
    main()
