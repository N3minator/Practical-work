# Простое Графическое Приложение
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

# Примечание: IDE PyCharm не знает о существовании self.cursor и self.execute. Из-а чего она выводит много предупреждений ибо она не может их распознать!

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

    def get_cursor(self):
        return self.cursor

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
        # Сохраняем логин пользователя перед закрытием окна
        self.user_login = self.login_entry.get().strip()

        #messagebox.showwarning('Осторожно!', 'Вы вошли как Гость!')
        self.open_library()

    # Реализуем функционал кнопки Сбросить Ввод
    def reset_fields(self):
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    # Функция для открытия окна Библиотеки Книг
    def open_library(self):
        # Сохраняем логин пользователя перед закрытием окна
        self.user_login = self.login_entry.get().strip()

        # Закрываем окно входа/регистрации
        self.root.destroy()
        # Инициализируем новое окно Библиотеки Книг
        win_booklibrary = tk.Tk()

        # Передача окна Библиотеки Книг/курсора/логина в класс BookLibrary
        BookLibrary(win_booklibrary, self.cursor,  self.conn, self.user_login)

        # Переименовываем программу
        win_booklibrary.title("Библиотека Книг")

        # Устанавливаем расширение по умолчанию
        win_booklibrary.geometry(f'325x200')
        # Запрещаем менять размер окна
        win_booklibrary.resizable(width=False, height=False)
        # Устанавливаем цвет фона приложения
        win_booklibrary['bg'] = 'black'

        # Режим ожидания
        win_booklibrary.mainloop()


class BookLibrary (tk.Frame):

    def __init__(self, win_library, cursor, connect, login):

        super().__init__(win_library)
        self.win_library = win_library
        self.cursor = cursor
        self.conn = connect
        self.login = login

        self.win_app_books = WinAppBooks()  # Объект класса WinAppBooks

        # Создание кнопки для меню выбора
        # Хочу потом сделать чтобы через цикл for выводился текст только для пользователей без админки, или если аккаунт под админкой то выводился текст дополнительно для Админов
        self.choice_label = tk.Label(win_library, text='''Что вы хотите сделать?
        1. Посмотреть доступные книги
        2. Посмотреть взятые книги пользователями (Админ)
        3. Взять на прокат
        4. Вернуть книгу
        5. Посмотреть ваш список взятых книг
        6. Добавить книгу (Админ)
        7. Удалить книгу (Админ)
        0. Выйти''')
        self.choice_label.grid(row=0, column=0)
        self.choice_entry = tk.Entry(win_library)
        self.choice_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.win_library.bind('<Return>', lambda event: self.choice())

    def choice(self):
        choice = self.choice_entry.get().strip()

        if choice == '1':
            # Открываем базу данных с доступными книгами
            self.cursor.execute("SELECT * FROM books WHERE visible=1")
            books = self.cursor.fetchall()

            if books:
                # Собираем информацию о книгах в одну строку
                books_info = '\n'.join(
                    [f"Номер книги: {book[0]} | Название книги: {book[1]} | Автор: {book[2]} | Жанр: {book[3]}\n" for book in books])
                messagebox.showinfo('Доступные книги', books_info)
            else:
                messagebox.showinfo('Доступные книги', 'В данный момент нет доступных книг.')
        elif choice == '2':
            # Ищем пользователя в базе данных
            self.cursor.execute("SELECT * FROM users WHERE login=?", (self.login,))
            state_user = self.cursor.fetchone()

            # Если результат не равен None, это означает, что пользователь найден (То что он не под Гостевым аккаунтом)
            if state_user is not None:
                # Открываем базу данных и ищем пользователя с таким логином и узнаем его статус Админа
                self.cursor.execute("SELECT admin_state FROM users WHERE login=?", (self.login,))
                state_admin = self.cursor.fetchone()

                if state_admin[0] == 'True':
                    self.list_rented_books()
                else:
                    messagebox.showerror('Отказ доступа!', 'Отказано в доступе! Вы не Админ!')
            else:
                messagebox.showerror('Ошибка!', 'Вы под Гостевым аккаунтом!')
        elif choice == '3':
            self.win_app_books.buy_books(self.cursor,  self.conn) # Вызываем метод buy_books() через объект WinAppBooks
        elif choice == '4':
            messagebox.showwarning('Недоступно!', 'На данный момент эта функция Разрабатывается!')
        elif choice == '5':
            messagebox.showwarning('Недоступно!', 'На данный момент эта функция Разрабатывается!')
        elif choice in ['6', '7']:
            # Ищем пользователя в базе данных
            self.cursor.execute("SELECT * FROM users WHERE login=?", (self.login,))
            state_user = self.cursor.fetchone()

            # Если результат не равен None, это означает, что пользователь найден (То что он не под Гостевым аккаунтом)
            if state_user is not None:
                self.cursor.execute("SELECT admin_state FROM users WHERE login=?", (self.login,))
                # if cursor.fetchone()[0] == 'True || Проверяет является ли пользователей Админом
                if self.cursor.fetchone()[0] == 'True':
                    if choice == "6":
                        self.win_app_books.add_book(self.cursor,  self.conn)  # Вызываем метод add_book() через объект WinAppBooks
                    else:
                        self.win_app_books.del_book()  # Вызываем метод add_book() через объект WinAppBooks
                else:
                    messagebox.showerror('Отказ доступа!', 'Отказано в доступе! Вы не Админ!')
            else:
                messagebox.showerror('Ошибка!', 'Вы под Гостевым аккаунтом!')
        elif choice == '0':
            # Закрываем окно Библиотеки Книг (Закрываем программу полностью)
            self.win_library.destroy()
        else:
            messagebox.showerror('Ошибка!', 'Вы ввели не верное число!')

    def list_rented_books(self):
        """Отображает список взятых книг."""
        self.cursor.execute("SELECT * FROM user_books")
        books = self.cursor.fetchall()

        if books:
            # Собираем информацию о книгах в одну строку
            books_info = '\n'.join(
                [f"ID Книги: {books[0]} | Название: {books[1]} | Автор: {books[2]} | Жанр: {books[3]} | Взято: {books[4]} | До: {books[5]} | Пользователь: {books[6]} | ID пользователя: {books[7]}\n" for book
                 in books])
            messagebox.showinfo('Доступные книги', books_info)
        else:
            messagebox.showwarning('Нету книг на прокате!', 'В данный момент не кто не взял книги :(')


class WinAppBooks:

    def buy_books(self, cursor, connect):
        self.cursor = cursor
        self.conn = connect

    def add_book(self, cursor, connect):
        self.cursor = cursor
        self.conn = connect
        # Инициализируем новое окно Добавление Книги
        win_add_book = tk.Tk()

        # Переименовываем программу
        win_add_book.title("Добавление Книги")

        # Устанавливаем расширение по умолчанию
        win_add_book.geometry(f'325x200')
        # Запрещаем менять размер окна
        win_add_book.resizable(width=False, height=False)
        # Устанавливаем цвет фона приложения
        win_add_book['bg'] = 'black'

        self.name_book_label = tk.Label(win_add_book, text="Введите название книги:")
        self.name_book_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_book_entry = tk.Entry(win_add_book)
        self.name_book_entry.grid(row=0, column=1, padx=10, pady=5)

        self.author_book_label = tk.Label(win_add_book, text="Введите автора книги:")
        self.author_book_label.grid(row=1, column=0, padx=10, pady=5)
        self.author_book_entry = tk.Entry(win_add_book)
        self.author_book_entry.grid(row=1, column=1, padx=10, pady=5)

        self.genre_book_label = tk.Label(win_add_book, text="Введите жанр книги:")
        self.genre_book_label.grid(row=2, column=0, padx=10, pady=5)
        self.genre_book_entry = tk.Entry(win_add_book)
        self.genre_book_entry.grid(row=2, column=1, padx=10, pady=5)

        self.visible_book_label = tk.Label(win_add_book, text='''Книга доступна для проката?
        (1 - да, 0 - нет):''')
        self.visible_book_label.grid(row=3, column=0, padx=10, pady=5)
        self.visible_book_entry = tk.Entry(win_add_book)
        self.visible_book_entry.grid(row=3, column=1, padx=10, pady=5)

        # Создание кнопки для Подтверждения
        self.confirmation_button = tk.Button(win_add_book, text="Подтверждения", command=lambda: self.confirmation_add(win_add_book))
        self.confirmation_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Режим ожидания
        win_add_book.mainloop()

    def confirmation_add(self, win):

        self.win_add_book = win

        # Получаем список существующих идентификаторов Книг
        self.cursor.execute("SELECT id_books FROM books ORDER BY id_books ASC")
        existing_ids = [id_[0] for id_ in self.cursor.fetchall()]

        # Находим первый свободный ID
        new_id = 1
        for id_ in existing_ids:
            if id_ != new_id:
                break
            new_id += 1

        name_book = self.name_book_entry.get()
        author_book = self.author_book_entry.get()
        genre_book = self.genre_book_entry.get()
        visible_book = self.visible_book_entry.get()

        # Проверяем валидность данных
        if not self.check_add_book(name_book, author_book, genre_book, visible_book):
            return

        self.cursor.execute("INSERT INTO books (id_books, name_books, author, genre, visible) VALUES (?, ?, ?, ?, ?)",
                       (new_id, name_book, author_book, genre_book, visible_book))
        self.conn.commit()

        messagebox.showinfo('Успех!', 'Вы добавили новую книгу!')

        # Закрываем окно Добавление Книг
        self.win_add_book.destroy()

    def check_add_book(self, name_book, author_book, genre_book, visible_book):

        # Чтобы получилось например из "  Vitalii    Derkach  " в "Vitalii Derkach"
        name_book = re.sub(r'\s+', ' ', name_book).strip()
        author_book = re.sub(r'\s+', ' ', author_book).strip()
        genre_book = re.sub(r'\s+', ' ', genre_book).strip()
        visible_book = re.sub(r'\s+', ' ', visible_book).strip()

        visible_book = int(visible_book)

        if name_book and author_book and genre_book:
            if visible_book == 1 or visible_book == 0 and visible_book is not None:
                return True
            else:
                messagebox.showerror('Ошибка!', 'Не правильное значение поля видимости!')
                return False
        else:
            messagebox.showerror('Ошибка!', 'Поля не могут быть пустыми!')
            return False

    def del_book(self):
        pass


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
