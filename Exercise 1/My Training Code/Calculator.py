import tkinter as tk
from tkinter import messagebox

# Эти заметки чисто для себя. Чтобы запомнить как работают функции

# row=0, column=1 || row - ряд || column - колонка
# sticky=tk.W || смешает на запад то есть в лево
# sticky=tk.E || смешает на восток то есть в право
# sticky=tk.CENTER || смешает в центр
# sticky='we' || от запада до востока, то есть расстягивает с лева на право
# sticky='wens' || растягивает по всем 4 сторонам света
# padx=10 || смешает в право || pady=10 || смешает вниз

# Функция отвечающая за кнопки от 0 до 9
def make_digit_button(digit):
    return tk.Button(win, text=digit, bd=5, font=('Arial', 10), command=lambda: add_digit(digit))

# Функция отвечающая за кнопки +-/*
def make_operation_button(operation):
    return tk.Button(win, text=operation, bd=5, font=('Arial', 13), fg='#11d911', bg='#D3D3D3', command=lambda: add_operation(operation))

# Функция отвечающая за кнопку =
def make_calc_button(operation):
    return tk.Button(win, text=operation, bd=5, font=('Arial', 13), fg='#ffffff', bg='#11d911', command=calculate)

# Функция отвечающая за кнопку С
def make_clear_button(operation):
    return tk.Button(win, text=operation, bd=5, font=('Arial', 13), fg='#fb2c03', bg='#939393', command=clear)

def add_digit(digit):

    value = calc.get()

    # Если мы начинаем вводить цифры то 0 по умолчанию автоматически удаляется. И если длинна строки равна 1 то 0 тоже удалиться ???
    if value[0] == '0' and len(value) == 1:
        value = value[1:]

    calc.delete(0, tk.END)
    calc.insert(0, value + digit)

def add_operation(operation):

    value = calc.get()

    if value[-1] in '+-/*':
        value = value[:-1]
    calc.delete(0, tk.END)
    calc.insert(0, value + operation)

def calculate():
    # Принимаем значения в вводе
    value = calc.get()
    # Удаляем все пробелы из строки. Тут метод .strip() не подходит потому что удаляет только начальные и конечные пробелы в строке, но не удаляет пробелы внутри строки.
    value = value.replace(' ', '')

    # Если пользователь введет например 15+ и сразу = то калькулятор посчитает это так 15+15=30
    if value[-1] in '+-/*':
        value = value+value[:-1]

    # Если последние два символа в строке / 0 то мы удаляем эти символы перед вычислением
    if value[-2] == '/' and value[-1] == '0':
        # Удаляем последние два символа
        messagebox.showerror("Ошибка", "Неверное выражение!")
        # Выходим из функции
        return

    # Проверяем, состоит ли строка только из цифр и разрешенных специальных знаков
    if all(char.isdigit() or char in '+-*/' for char in value):
        # Очищаем поле ввода
        calc.delete(0, tk.END)
        # Высчитываем и выводим результат
        calc.insert(0, eval(value))
    else:
        # Показываем сообщение об ошибке
        messagebox.showerror("Ошибка", "Неверное выражение!")
        # Выходим из функции
        return

def clear():
    calc.delete(0, tk.END)
    calc.insert(0, '0')

# Создаём графическое поле
win = tk.Tk()
# Переименовываем программу
win.title('Calculator')
# Устанавливаем расширение по умолчанию
win.geometry(f'238x265+100+200')
# Устанавливаем цвет фона приложения
win['bg'] = 'black'

# Ввод || justify=tk.LEFT - это свойство которое приказывает тексту прижыматься к левой стороне
# width=15 || параметр указывает на количество символов, которые можно ввести в поле ввода Entry перед тем, как оно начнет автоматически переносить текст на новую строку
calc = tk.Entry(win, justify=tk.LEFT, font=('Arial', 15), width=15)

# Приписываем 0 в строку при запуске калькулятора
calc.insert(0, '0')

# Поле ввода || Атрибут columnspan обьеденяет несколько колонок
# stick='we' || растягивает введёные цифры
calc.grid(row=0, column=0, columnspan=4, stick='we')

# Наши кнопки от 0 до 9 и не только...

# padx=5, pady=5 отвечает за расстрояние между кнопками
# bd=5 отвечает за толщину рамок || stick='wens' || расстягивает кнопки

make_digit_button('1').grid(row=1, column=0, stick='wens', padx=5, pady=5)
make_digit_button('2').grid(row=1, column=1, stick='wens', padx=5, pady=5)
make_digit_button('3').grid(row=1, column=2, stick='wens', padx=5, pady=5)
make_digit_button('4').grid(row=2, column=0, stick='wens', padx=5, pady=5)
make_digit_button('5').grid(row=2, column=1, stick='wens', padx=5, pady=5)
make_digit_button('6').grid(row=2, column=2, stick='wens', padx=5, pady=5)
make_digit_button('7').grid(row=3, column=0, stick='wens', padx=5, pady=5)
make_digit_button('8').grid(row=3, column=1, stick='wens', padx=5, pady=5)
make_digit_button('9').grid(row=3, column=2, stick='wens', padx=5, pady=5)
make_digit_button('0').grid(row=4, column=1, stick='wens', padx=5, pady=5)

make_operation_button('-').grid(row=4, column=0, stick='wens', padx=5, pady=5)
make_operation_button('+').grid(row=4, column=2, stick='wens', padx=5, pady=5)

make_clear_button('C').grid(row=1, column=3, stick='wens', padx=5, pady=5)

make_operation_button('/').grid(row=2, column=3, stick='wens', padx=5, pady=5)
make_operation_button('*').grid(row=3, column=3, stick='wens', padx=5, pady=5)

make_calc_button('=').grid(row=4, column=3, stick='wens', padx=5, pady=5)

# Это делается для того, чтобы задать минимальную ширину колонок, чтобы они не сжимались слишком сильно, когда пользователь изменяет размер окна или когда в них размещаются виджеты.
# Так же они влияют на размер кнопок в правом концу
win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=60)

#  Строка сетки не будет сжиматься по вертикали до размера меньше 60 пикселей, даже если в ней нет содержимого или если пользователь изменит размер окна.
win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)

# Режим ожидания
win.mainloop()