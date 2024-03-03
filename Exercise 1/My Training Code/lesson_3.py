import tkinter as tk

count = 0

def say_hello():
    print('Hello')

def add_label(win):
    label_1 = tk.Label(win, text='new')
    label_1.pack()

def counter(bth4):

    # Делаем перменную count видимой для всех функций
    global count

    count += 1
    bth4['text'] = f'Счетчик {count}'

def Disable(bth4):

    # Узнаём состояние кнопки bth4
    current_state = bth4.cget('state')

    # Метод config используется для изменения различные атрибут виджета, таких как текст, цвет, шрифт, состояние и т.д.
    if current_state == tk.NORMAL:
        bth4.config(state=tk.DISABLED)
        bth4.config(text='Enable bth4')
    else:
        bth4.config(state=tk.NORMAL)
        bth4.config(text=f'Счетчик {count}')

def main():
    # Создание графического окна
    win = tk.Tk()

    # Устанавливаем стандартное разрешение экрана приложения при запуске программы
    win.geometry('1920x1080')

    # Меняем описание программы
    win.title('Графическое приложение')

    # Изменяем иконку приложения
    photo = tk.PhotoImage(file='calculator.png')
    win.iconphoto(False, photo)

    # Создаем текст с координатами x и y, шириной 20, высотой 5 и шрифтом Arial размером 10 с жирным начертанием
    label_1 = tk.Label(win, text='Добро пожаловать!', width=20, height=5, font=('Arial', 10, 'bold'))

    # Вызываем переменную с текстом и присваиваем ей заданные координаты
    label_1.pack(anchor='e')
    label_1.pack(anchor='w')

    # Создаем кнопку "Hi" с командой say_hello
    bth1 = tk.Button(win, text='Hi', command=say_hello)
    bth1.pack()

    # Создаем кнопку "Hi" с командой add_label и передаем объект окна win
    bth2 = tk.Button(win, text='Add new label', command=lambda: add_label(win))
    bth2.pack()

    bth3 = tk.Button(win, text='Add lambda', command=lambda: tk.Label(win, text='New lambda').pack())
    bth3.pack()

    bth4 = tk.Button(win, text=f'Счетчик {count}', command=lambda: counter(bth4))
    bth4.pack()

    bth5 = tk.Button(win, text='Normal/Dissabel bth4', command=lambda: Disable(bth4))
    bth5.pack()

    # Чтобы наша программа была постоянно в режиме ожидания, как в цикле
    win.mainloop()

if __name__ == "__main__":
    main()
