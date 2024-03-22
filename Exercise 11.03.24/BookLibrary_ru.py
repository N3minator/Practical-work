# Задание на Python
#
# Все книги должны храниться в базе данных MySQL.
#
# Функционал, которому должно соответствовать приложение:
#
# 1. Регистрация пользователя:
#
# Он позволяет пользователям создавать учетные записи и входить в систему.
#
# Каждая учетная запись может иметь свои уникальные данные, такие как имя, фамилия, адрес электронной почты и т. д.
#
# Два типа учетных записей: администратор и пользователь. Администраторы имеют возможность добавлять новые книги.
#
# 2. Просмотр книг:
#
# Пользователи могут просматривать доступные книги в библиотеке.
#
# (опционально) Возможность сортировать и фильтровать книги по различным категориям (например, жанру, автору, названию).
#
# 3. Поиск книг:
#
# Функция поиска позволяет пользователям быстро находить конкретные книги по названию, автору, жанру и т. д.
#
# 4. Беру книги напрокат:
#
# Пользователи могут брать книги, имеющиеся в библиотеке.
#
# Система проверяет наличие книги перед тем, как взять ее напрокат
#
# После заимствования пользователю назначается срок возврата книги.
#
# 5. Возврат книг:
#
# Пользователи могут вернуть взятые напрокат книги до истечения установленного срока.
#
# Система обновляет статус доступности книги после ее возврата.
#
# 6. Добавляем новые книги:
#
# Администраторы библиотеки могут добавлять в каталог новые книги.
#
# Каждая книга содержит такую информацию, как название, автор, краткое описание, необязательно: фото на обложке.
#
# 7. Управление статусом библиотеки:
#
# Администраторы могут управлять состоянием библиотеки, добавляя новые книги, обновляя сведения о существующих книгах, удаляя книги и т. д.

"Простое Графическое Приложение"
import tkinter as tk
# Для вывода сообщений на экран
from tkinter import messagebox
# Для работы с базами данных
import sqlite3
# Обработчик текста
import re
# Для хэширования важных данных
import bcrypt
# Для генерации случайных цифр
import random



class LoginRegisterApp:

    def __init__(self, root):
        # Инициализация приложения входа/регистрации с переданным корневым (главным) окном
        self.root = root
        self.root.title("Вход / Регистрация")

        # Создание меток и полей для ввода логина и пароля и gmail
        self.login_label = tk.Label(root, text="Логин:")
        self.login_label.grid(row=0, column=0, padx=10, pady=5)
        self.login_entry = tk.Entry(root)
        self.login_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(root, text="Пароль:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.gmail_label = tk.Label(root, text='Gmail:')
        self.gmail_label.grid(row=2, column=0, padx=10, pady=5)
        self.gmail_entry = tk.Entry(root)
        self.gmail_entry.grid(row=2, column=1, padx=10, pady=5)

        # Добавляем функции на Клавиши клавиатуры в поле ввода
        self.login_entry.bind("<Return>", lambda event: self.focus_next_widget(self.password_entry))
        self.password_entry.bind("<Return>", lambda event: self.focus_next_widget(self.gmail_entry))
        self.gmail_entry.bind("<Return>", self.perform_login)

        # Добавление галочки для отображения пароля
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(root, text="Показать пароль", variable=self.show_password_var,
                                                     command=self.toggle_password_visibility)
        self.show_password_checkbox.grid(row=1, column=2, padx=5)

        # Добавление пропуска регистрации
        self.skip_register = tk.BooleanVar()
        self.skip_register_checkbox = tk.Checkbutton(root, text='Пропустить регистрацию', variable=self.skip_register,
                                                     command=self.skip_register_user)
        self.skip_register_checkbox.grid(row=0, column=2, padx=5)

        # Создание кнопок для входа и регистрации и Gmail
        self.login_button = tk.Button(root, text="Войти",
                                      command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.register_button = tk.Button(root, text="Зарегистрироваться",
                                         command=self.register)
        self.register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Добавляем кнопку сброса
        self.reset_button = tk.Button(root, text="Сбросить ввод",
                                      command=self.reset_fields)
        self.reset_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # conn и cursor инициализируются в конструкторе класса __init__, а затем используются в функциях login и register без необходимости передачи их в качестве аргументов в (). Это делает код более чистым и читаемым, и предотвращает дублирование кода.
        # Подключение к базе данных и создание курсора
        self.conn = sqlite3.connect('BookLibrary.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def focus_next_widget(self, widget):
        """Перемещает фокус на следующий виджет."""
        widget.focus_set()

    def perform_login(self, event):
        """Вызывает метод login при нажатии Enter в поле ввода Gmail."""
        self.login()

    def create_tables(self):
        """Создает таблицы в базе данных."""
        with sqlite3.connect('BookLibrary.db') as conn:
            # Хранение книг
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS books
                              (id_books INTEGER PRIMARY KEY, name_books TEXT, author TEXT, genre TEXT, visible BOOLEAN)''')
            # Хранение данных пользователей
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                              (id_users INTEGER PRIMARY KEY, login TEXT, password_hash TEXT, gmail_user TEXT, admin_state TEXT)''')
            # Хранение данных пользователей которые взяли книги
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_books
                              (id_users INTEGER,
                               login TEXT,
                               id_books INTEGER,
                               date_rented TIMESTAMP, 
                               return_date TIMESTAMP,
                               FOREIGN KEY (id_users) REFERENCES users(id_users),
                               FOREIGN KEY (id_books) REFERENCES books(id_books))''')
            conn.commit()

    # Про функцию чтобы ввести либо Логин или Gmail я подумал слишком поздно. А чтобы это реализовать надо очень много кода переделать
    def login(self):
        # Метод для обработки входа пользователя
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        gmail = self.gmail_entry.get().strip()

        # Проверяем валидность данных
        if not self.validate_data(login, password, gmail):
            return

        self.cursor.execute("SELECT password_hash FROM users WHERE login=?", (login,))
        user = self.cursor.fetchone()

        # Сравниваем введенный пароль и пароль который храниться в базе данных аккаунта в которого пользователь хочет зайти
        if user:
            if bcrypt.checkpw(password.encode(), user[0]):
                messagebox.showinfo("Успех", "Вход выполнен успешно!")
                self.open_library()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")
        else:
            messagebox.showerror("Ошибка", "Данного пользователя не существует!")

    def register(self):
        # Метод для обработки регистрации нового пользователя
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        gmail = self.gmail_entry.get().strip()

        # Проверка валидности данных и получение обновленного gmail
        validation_result, gmail = self.validate_data(login, password, gmail)
        if not validation_result:
            return

        # Узнаем существуют ли такие пользователи с данным Логином и Gmail
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE login = ? OR gmail_user = ?", (login, gmail))

        # Если пользователя с таким Логином и Gmail не существует. То создаётся аккаунт
        if self.cursor.fetchone()[0] == 0:
            # Хеширование пароля
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            while True:
                user_id_str = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                user_id = int(user_id_str)
                self.cursor.execute("SELECT COUNT(*) FROM users WHERE id_users = ?", (user_id_str,))

                # Если пользователя с таким генерируемым ID не существует. То завершаем цикл генерации ID
                if self.cursor.fetchone()[0] == 0:
                    del user_id_str
                    break

            admin_state = 'False'

            # Добавляем нового пользователя
            self.cursor.execute(
                "INSERT INTO users (id_users, login, password_hash, gmail_user, admin_state) VALUES (?, ?, ?, ?, ?)",
                (user_id, login, hashed_password, gmail, admin_state))
            self.conn.commit()

            messagebox.showinfo("Регистрация", "Регистрация успешна!")
            self.open_library()
        else:
            # Проверяем, какой параметр вызвал конфликт при регистрации
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE login = ?", (login,))
            login_count = self.cursor.fetchone()[0]

            if login_count > 0:
                messagebox.showerror('Ошибка!', 'Пользователь с таким Логином уже существует!')
            else:
                messagebox.showerror('Ошибка!', 'Пользователь с таким Gmail уже существует!')

    # Добавляем функцию для валидации данных
    def validate_data(self, login, password, gmail):

        # Чтобы получилось например из "  Vitalii    Derkach  " в "Vitalii Derkach"
        login = re.sub(r'\s+', ' ', login).strip()
        # Этот метод удаляет только вначале и конце пробелы. Но внутри пробелы он оставляет без изменений
        password = re.sub(r'^\s+|\s+$', '', password)
        # Обрабатываем лишние пробелы в поле ввода Gmail
        gmail = re.sub(r'\s+', ' ', gmail).strip()

        # Добавляем "@gmail.com", если его нет в адресе электронной почты
        if not gmail.endswith('@gmail.com'):
            gmail += '@gmail.com'
        if not login or not password:
            messagebox.showwarning("Предупреждение", "Логин и пароль не могут быть пустыми.")
            return False
        elif len(password) < 8:
            messagebox.showwarning("Предупреждение", "Пароль должен содержать минимум 8 символов.")
            return False
        elif login.isdigit() or password.isdigit():
            messagebox.showwarning("Предупреждение", "Логин и пароль не могут состоять только из цифр.")
            return False
        else:
            # Возвращаем обновленное значение gmail
            return True, gmail


    # Реализуем функционал кнопки Показать Пароль
    def toggle_password_visibility(self):
        # Функция для переключения режима отображения пароля
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    # Реализуем функционал кнопки Пропустить Регистрацию
    def skip_register_user(self):
        messagebox.showwarning('Осторожно!', 'Вы вошли как Гость!')
        self.open_library()

    # Реализуем функционал кнопки Сбросить Ввод
    def reset_fields(self):
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    # Функция для открытия окна калькулятора
    def open_library(self):
        # Закрываем окно входа/регистрации
        self.root.destroy()
        # Функция для открытия окна калькулятора
        calc_win = tk.Tk()

        # Передача окна калькулятора в класс BookLibrary
        BookLibrary(calc_win)

        # Переименовываем программу
        calc_win.title("Библиотека Книг")

        # Устанавливаем расширение по умолчанию
        calc_win.geometry(f'238x265')
        # Запрещаем менять размер окна
        calc_win.resizable(width=False, height=False)
        # Устанавливаем цвет фона приложения
        calc_win['bg'] = 'black'

        # Режим ожидания
        calc_win.mainloop()


class BookLibrary (tk.Frame):

    def __init__(self, root):
        print('hi')


def open_login_register():
    # Function to open the login/register window
    login_register_window = tk.Tk()
    # Prevent resizing of the login/register window
    login_register_window.resizable(width=False, height=False)
    # Pass the registration window to the LoginRegisterApp class
    LoginRegisterApp(login_register_window)
    # Run in a loop
    login_register_window.mainloop()


if __name__ == "__main__":
    open_login_register()
