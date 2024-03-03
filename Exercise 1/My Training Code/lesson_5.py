import tkinter as tk

# Знакомство с виджетами Entry

# row=0, column=1 || row - ряд || column - колонка
# sticky=tk.W || смешает на запад то есть в лево
# sticky=tk.E || смешает на восток то есть в право
# sticky=tk.CENTER || смешает в центр
# sticky='we' || от запада до востока, то есть расстягивает с лева на право
# padx=10 || смешает в право || pady=10 || смешает вниз


def get_entry():
    # Присваиваем к переменной имя которое он написал в строке
    value = name.get()

    if value:
        # Выводим имя пользователя которое он вписал
        print(value)
    else:
        print('Emptry Entry')

def delete_entry():
    # С 0 до 3 удалить ряды или ввести за месть 3 'end' или tk.END - то есть под самый конец удалить
    name.delete(0, tk.END)

def sumbit():
    print(f'Имя -> {name.get()}')
    print(f'Пароль -> {password.get()}')

    # Вызываем функцию которая удаляет строку имени
    delete_entry()
    # Тут через метод delete удаляем строку password от 0 строки до конца
    password.delete(0, tk.END)


# Создаём графическое поле
win = tk.Tk()
# Переименовываем программу
win.title('Lesson 5')

# Создаём поле ввода имени
tk.Label(win, text='Name').grid(row=0, column=0, sticky=tk.W, padx=10)
name = tk.Entry(win)
name.grid(row=0, column=1)

# Создаём поле ввода пароля
tk.Label(win, text='Пароль').grid(row=1, column=0, sticky=tk.W, padx=10)
# show='*' скрывает пароль этим символом *
password = tk.Entry(win, show='*')
password.grid(row=1, column=1)

# Создаём кнопки
tk.Button(win, text='get', command=get_entry).grid(row=2, column=0, stick='we')
tk.Button(win, text='delete', command=delete_entry).grid(row=2, column=1, stick='we')
tk.Button(win, text='insert', command=lambda: name.insert(tk.END, 'hello')).grid(row=2, column=2, stick='we')
tk.Button(win, text='Sumbit', command=sumbit).grid(row=3, column=1, stick='we')


# Это делается для того, чтобы задать минимальную ширину колонок, чтобы они не сжимались слишком сильно, когда пользователь изменяет размер окна или когда в них размещаются виджеты.
win.grid_columnconfigure(0, minsize=30)
win.grid_columnconfigure(1, minsize=30)

# Режим ожидания
win.mainloop()