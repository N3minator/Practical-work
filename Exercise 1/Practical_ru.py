import tkinter as tk
from tkinter import messagebox
import sqlite3
from cryptography.fernet import Fernet
import re

class LoginRegisterApp:

    def __init__(self, root):
        # Инициализация приложения входа/регистрации с переданным корневым (главным) окном
        self.root = root
        self.root.title("Вход / Регистрация")

        # Генерация ключа шифрования
        self.key = Fernet.generate_key()

        # Создание меток и полей для ввода логина и пароля
        self.username_label = tk.Label(root, text="Логин:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(root, text="Пароль:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Добавление галочки для отображения пароля
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(root, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_checkbox.grid(row=1, column=2, padx=5)

        # Создание кнопок для входа и регистрации
        self.login_button = tk.Button(root, text="Войти", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.register_button = tk.Button(root, text="Зарегистрироваться", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Создание базы данных пользователей, если она еще не существует
        self.create_database()

    def toggle_password_visibility(self):
        # Функция для переключения режима отображения пароля
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def create_database(self):
        # Создание таблицы пользователей в базе данных SQLite, если она еще не существует
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT,
                            password TEXT
                        )''')
        connection.commit()
        connection.close()

    def login(self):
        # Метод для обработки входа пользователя
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Чтобы получилось например из "  Vitalii    Derkach  " в "Vitalii Derkach"
        username = re.sub(r'\s+', ' ', username).strip()

        # Этот метод удаляет только вначале и конце пробелы. Но внутри пробелы он оставляет без изменений
        password = re.sub(r'^\s+|\s+$', '', password)

        if username.isdigit():
            messagebox.showerror("Ошибка", "Логин не может состоять только из цифр!")
            return

        # Подключение к базе данных и выполнение запроса
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Извлечение пользователя из базы данных по его имени пользователя
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            # Если пользователь найден, извлекаем зашифрованный пароль из базы данных
            stored_password = user[2]

            # Расшифровываем зашифрованный пароль с использованием ключа
            cipher_suite = Fernet(self.key)
            decrypted_password = cipher_suite.decrypt(stored_password).decode()

            # Проверяем, совпадает ли введенный пароль с дешифрованным паролем из базы данных
            if password == decrypted_password:
                messagebox.showinfo("Успех", "Вход выполнен успешно!")
                self.open_calculator()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

        connection.close()

    def check_password(self, password, stored_password):
        # Метод для проверки пароля пользователя
        # Шифрование введенного пароля для сравнения с сохраненным
        cipher_suite = Fernet(Fernet.generate_key())
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password == stored_password

    def register(self):
        # Метод для обработки регистрации нового пользователя
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Чтобы получилось например из "  Vitalii    Derkach  " в "Vitalii Derkach"
        username = re.sub(r'\s+', ' ', username).strip()

        # Этот метод удаляет только вначале и конце пробелы. Но внутри пробелы он оставляет без изменений
        password = re.sub(r'^\s+|\s+$', '', password)

        if username.isdigit():
            messagebox.showerror("Ошибка", "Логин не может состоять только из цифр!")
            return
        elif password.isdigit():
            messagebox.showerror("Ошибка", "Пароль не может состоять только из цифр!")
            return
        elif len(password) < 8:
            messagebox.showerror("Ошибка", "Пароль должен содержать минимум 8 символов!")
            return


        # Шифрование пароля с использованием ключа
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode())

        # Подключение к базе данных и выполнение запроса
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Вставка нового пользователя в базу данных
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
        connection.commit()
        connection.close()

        messagebox.showinfo("Регистрация", "Регистрация успешна!")
        self.root.after(100, self.open_calculator)

    # Функция для открытия окна калькулятора
    def open_calculator(self):
        # Закрываем окно входа/регистрации
        self.root.destroy()
        # Функция для открытия окна калькулятора
        calc_win = tk.Tk()

        # Передача окна калькулятора в CalculatorApp
        app = CalculatorApp(calc_win)

        # Переименовываем программу
        calc_win.title("Калькулятор")

        # Устанавливаем расширение по умолчанию
        calc_win.geometry(f'238x265')
        # Запрещаем менять размер окна
        calc_win.resizable(width=False, height=False)
        # Устанавливаем цвет фона приложения
        calc_win['bg'] = 'black'

        # Режим ожидания
        calc_win.mainloop()

class CalculatorApp(tk.Frame):

    def __init__(self, calc_win):
        super().__init__(calc_win)
        self.calc_win = calc_win

        # Ввод || justify=tk.LEFT - это свойство которое приказывает тексту прижыматься к левой стороне
        # width=15 || параметр указывает на количество символов, которые можно ввести в поле ввода Entry перед тем, как оно начнет автоматически переносить текст на новую строку
        self.calc = tk.Entry(calc_win, justify=tk.LEFT, font=('Arial', 15), width=15)

        # Приписываем 0 в строку при запуске калькулятора
        self.calc.insert(0, '0')

        # Размещение поля ввода на главном окне
        # Поле ввода || Атрибут columnspan обьеденяет несколько колонок
        self.calc.grid(row=0, column=0, columnspan=4, stick='we')

        # padx=5, pady=5 отвечает за расстрояние между кнопками
        # bd=5 отвечает за толщину рамок || stick='wens' || расстягивает кнопки
        self.make_digit_button('1').grid(row=1, column=0, stick='wens', padx=5, pady=5)
        self.make_digit_button('2').grid(row=1, column=1, stick='wens', padx=5, pady=5)
        self.make_digit_button('3').grid(row=1, column=2, stick='wens', padx=5, pady=5)
        self.make_digit_button('4').grid(row=2, column=0, stick='wens', padx=5, pady=5)
        self.make_digit_button('5').grid(row=2, column=1, stick='wens', padx=5, pady=5)
        self.make_digit_button('6').grid(row=2, column=2, stick='wens', padx=5, pady=5)
        self.make_digit_button('7').grid(row=3, column=0, stick='wens', padx=5, pady=5)
        self.make_digit_button('8').grid(row=3, column=1, stick='wens', padx=5, pady=5)
        self.make_digit_button('9').grid(row=3, column=2, stick='wens', padx=5, pady=5)
        self.make_digit_button('0').grid(row=4, column=1, stick='wens', padx=5, pady=5)

        self.make_operation_button('-').grid(row=4, column=0, stick='wens', padx=5, pady=5)
        self.make_operation_button('+').grid(row=4, column=2, stick='wens', padx=5, pady=5)

        self.make_clear_button('C').grid(row=1, column=3, stick='wens', padx=5, pady=5)

        self.make_operation_button('/').grid(row=2, column=3, stick='wens', padx=5, pady=5)
        self.make_operation_button('*').grid(row=3, column=3, stick='wens', padx=5, pady=5)

        self.make_calc_button('=').grid(row=4, column=3, stick='wens', padx=5, pady=5)

        # При нажатии Enter на клавиатуре в строке. То калькулятор начинает выводить результат без нажатия кнопки =
        # `<Return>` обозначает клавишу Enter на клавиатуре
        self.calc_win.bind('<Return>', lambda event: self.calculate())

        # Чтобы при вводе с клавиатуры в строку от 0 до 9 цифра 0 по умолчанию удалялась
        self.calc.bind('1', self.add_keyboard_digit)
        self.calc.bind('2', self.add_keyboard_digit)
        self.calc.bind('3', self.add_keyboard_digit)
        self.calc.bind('4', self.add_keyboard_digit)
        self.calc.bind('5', self.add_keyboard_digit)
        self.calc.bind('6', self.add_keyboard_digit)
        self.calc.bind('7', self.add_keyboard_digit)
        self.calc.bind('8', self.add_keyboard_digit)
        self.calc.bind('9', self.add_keyboard_digit)
        self.calc.bind('0', self.add_keyboard_digit)

        # Чтобы при нажатии на клавиатуре клавишы С поле ввода очищалось
        self.calc_win.bind('c', lambda event: self.clear())
        self.calc_win.bind('C', lambda event: self.clear())

        # Это делается для того, чтобы задать минимальную ширину колонок, чтобы они не сжимались слишком сильно, когда пользователь изменяет размер окна или когда в них размещаются виджеты.
        # Так же они влияют на размер кнопок в правом концу
        self.calc_win.grid_columnconfigure(0, minsize=60)
        self.calc_win.grid_columnconfigure(1, minsize=60)
        self.calc_win.grid_columnconfigure(2, minsize=60)
        self.calc_win.grid_columnconfigure(3, minsize=60)

        #  Строка сетки не будет сжиматься по вертикали до размера меньше 60 пикселей, даже если в ней нет содержимого или если пользователь изменит размер окна.
        self.calc_win.grid_rowconfigure(1, minsize=60)
        self.calc_win.grid_rowconfigure(2, minsize=60)
        self.calc_win.grid_rowconfigure(3, minsize=60)
        self.calc_win.grid_rowconfigure(4, minsize=60)


    def make_digit_button(self, digit):
        return tk.Button(self.calc_win, text=digit, bd=5, font=('Arial', 10), command=lambda: self.add_digit(digit))

    def add_digit(self, digit):

        value = self.calc.get()

        # Если первый символ - '0' и длина строки равна 1, удаляем '0' и добавляем новую цифру
        if value[0] == '0' and len(value) == 1:
            value = value[1:]

        # Очистка поля ввода и добавление новой цифры
        self.calc.delete(0, tk.END)
        self.calc.insert(0, value + digit)

    def add_keyboard_digit(self, event):
        value = self.calc.get()
        if value[0] == '0' and len(value) == 1:
            self.calc.delete(0, tk.END)

    def make_operation_button(self, operation):
        return tk.Button(self.calc_win, text=operation, bd=5, font=('Arial', 13), fg='#11d911', bg='#D3D3D3',command=lambda: self.add_operation(operation))

    def add_operation(self, operation):
        value = self.calc.get()

        if value[-1] in '+-/*':
            value = value[:-1]
        self.calc.delete(0, tk.END)
        self.calc.insert(0, value + operation)

    def make_clear_button(self, operation):
        return tk.Button(self.calc_win, text=operation, bd=5, font=('Arial', 13), fg='#fb2c03', bg='#939393', command=self.clear)

    def clear(self):
        self.calc.delete(0, tk.END)
        self.calc.insert(0, '0')

    def make_calc_button(self, operation):
        return tk.Button(self.calc_win, text=operation, bd=5, font=('Arial', 13), fg='#ffffff', bg='#11d911', command=self.calculate)

    def calculate(self):
        # Принимаем значения в вводе
        value = self.calc.get()
        # Удаляем все пробелы из строки. Тут метод .strip() не подходит потому что удаляет только начальные и конечные пробелы в строке, но не удаляет пробелы внутри строки.
        value = value.replace(' ', '')

        # Если пользователь введет например 15+ и сразу активирует = то калькулятор посчитает это так 15+15=30
        if value[-1] in '+-/*':
            value = value + value[:-1]

        # Этот код разделяет строку по символу '/', а затем проверяет, является ли последний элемент после разделения равным '0'. Если да, то выводится сообщение об ошибке о делении на ноль.
        if '/' in value:
            parts = value.split('/')
            if len(parts) > 1 and parts[-1] == '0':
                messagebox.showerror("Ошибка", "Деление на ноль!")
                return

        # Проверяем, состоит ли строка только из цифр или разрешенных специальных знаков
        if all(char.isdigit() or char in '+-*/.' for char in value):
            # Очищаем поле ввода
            self.calc.delete(0, tk.END)
            # Высчитываем и выводим результат || функция eval считывает даже str строку
            self.calc.insert(0, eval(value))
        else:
            # Показываем сообщение об ошибке
            messagebox.showerror("Ошибка", "Неверное выражение!")
            # Выходим из функции
            return

def open_login_register():
    # Функция для открытия окна входа/регистрации
    login_register_window = tk.Tk()
    app = LoginRegisterApp(login_register_window)
    login_register_window.mainloop()

if __name__ == "__main__":
    open_login_register()
