import tkinter as tk

# row=0, column=1 || row - ряд || column - колонка
# sticky=tk.W || смешает на запад то есть в лево
# sticky=tk.E || смешает на восток то есть в право
# sticky=tk.CENTER || смешает в центр
# sticky='we' || от запада до востока, то есть расстягивает с лева на право
# sticky='wens' || растягивает по всем 4 сторонам света
# padx=10 || смешает в право || pady=10 || смешает вниз


# 1. `value = calc.get() + str(digit)`: В этой строке переменной `value` присваивается текущее содержимое поля ввода `calc`, полученное с помощью метода `.get()`
# А затем к этому содержимому добавляется введенная цифра. Переобразовывая цифры в строку выполняя с помощью `str(digit)`.
#
# 2. `calc.delete(0, tk.END)`: Эта строка удаляет текущее содержимое поля ввода `calc` от начала (индекс 0) до конца (`tk.END`), чтобы очистить его перед добавлением новой цифры.
# Это нужно, чтобы не добавлять новые цифры к старым, а заменить их на новые.
#
# 3. `calc.insert(0, value)`: Эта строка вставляет новое значение `value` в поле ввода `calc` в позицию с индексом 0, что означает вставку в начало поля ввода.
# Таким образом, после выполнения этой строки в поле ввода будет содержаться новое значение, состоящее из предыдущего содержимого и введенной цифры.
def add_digit(digit):

    value = calc.get() + str(digit)
    calc.delete(0, tk.END)
    calc.insert(0, value)


# Создаём графическое поле
win = tk.Tk()
# Переименовываем программу
win.title('lesson 6')
# Устанавливаем расширение по умолчанию
win.geometry(f'240x260+100+200')
# Устанавливаем цвет фона приложения
win['bg'] = 'black'

# Ввод || justify=tk.LEFT - это свойство которое приказывает тексту прижыматься к левой стороне
# width=15 || параметр указывает на количество символов, которые можно ввести в поле ввода Entry перед тем, как оно начнет автоматически переносить текст на новую строку
calc = tk.Entry(win, justify=tk.LEFT, font=('Arial', 15), width=15)

# Поле ввода || Атрибут columnspan обьеденяет несколько колонок
# stick='we' || растягивает введёные цифры
calc.grid(row=0, column=0, columnspan=4, stick='we')

# Наши кнопки от 0 до 9 и не только...
# padx=5, pady=5 отвечает за расстрояние между кнопками
# bd=5 отвечает за толщину рамок || stick='wens' || расстягивает кнопки
tk.Button(win, text='1', bd=5, font=('Arial', 10), command=lambda: add_digit(1)).grid(row=1, column=0, stick='wens', padx=5, pady=5)
tk.Button(win, text='2', bd=5, font=('Arial', 10), command=lambda: add_digit(2)).grid(row=1, column=1, stick='wens', padx=5, pady=5)
tk.Button(win, text='3', bd=5, font=('Arial', 10), command=lambda: add_digit(3)).grid(row=1, column=2, stick='wens', padx=5, pady=5)
tk.Button(win, text='4', bd=5, font=('Arial', 10), command=lambda: add_digit(4)).grid(row=2, column=0, stick='wens', padx=5, pady=5)
tk.Button(win, text='5', bd=5, font=('Arial', 10), command=lambda: add_digit(5)).grid(row=2, column=1, stick='wens', padx=5, pady=5)
tk.Button(win, text='6', bd=5, font=('Arial', 10), command=lambda: add_digit(6)).grid(row=2, column=2, stick='wens', padx=5, pady=5)
tk.Button(win, text='7', bd=5, font=('Arial', 10), command=lambda: add_digit(7)).grid(row=3, column=0, stick='wens', padx=5, pady=5)
tk.Button(win, text='8', bd=5, font=('Arial', 10), command=lambda: add_digit(8)).grid(row=3, column=1, stick='wens', padx=5, pady=5)
tk.Button(win, text='9', bd=5, font=('Arial', 10), command=lambda: add_digit(9)).grid(row=3, column=2, stick='wens', padx=5, pady=5)
tk.Button(win, text='0', bd=5, font=('Arial', 10), command=lambda: add_digit(0)).grid(row=4, column=1, stick='wens', padx=5, pady=5)

tk.Button(win, text='-', bd=5, font=('Arial', 10), command=lambda: add_digit('-'), fg='#11d911', bg='#D3D3D3').grid(row=4, column=0, stick='wens', padx=5, pady=5)
tk.Button(win, text='+', bd=5, font=('Arial', 10), command=lambda: add_digit('+'), fg='#11d911', bg='#D3D3D3').grid(row=4, column=2, stick='wens', padx=5, pady=5)
tk.Button(win, text='=', bd=5, font=('Arial', 10), command=lambda: add_digit('='), fg='white', bg='#11d911').grid(row=4, column=3, stick='wens', padx=5, pady=5)

tk.Button(win, text='C', bd=5, font=('Arial', 10), command=lambda: add_digit('C'), fg='red', bg='#D3D3D3').grid(row=1, column=3, stick='wens', padx=5, pady=5)
tk.Button(win, text='/', bd=5, font=('Arial', 10), command=lambda: add_digit('/'), fg='#11d911', bg='#D3D3D3').grid(row=2, column=3, stick='wens', padx=5, pady=5)
tk.Button(win, text='%', bd=5, font=('Arial', 10), command=lambda: add_digit('%'), fg='#11d911', bg='#D3D3D3').grid(row=3, column=3, stick='wens', padx=5, pady=5)

# Это делается для того, чтобы задать минимальную ширину колонок, чтобы они не сжимались слишком сильно, когда пользователь изменяет размер окна или когда в них размещаются виджеты.
win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)

#  Строка сетки не будет сжиматься по вертикали до размера меньше 60 пикселей, даже если в ней нет содержимого или если пользователь изменит размер окна.
win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)

# Режим ожидания
win.mainloop()