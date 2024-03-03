import tkinter as tk

win = tk.Tk()
win.geometry(f'1920x1080')
win.title('Урок 4')

bth1 = tk.Button(win, text= 'Hello 1')
bth2 = tk.Button(win, text= 'Hello 2')
bth3 = tk.Button(win, text= 'Hello 3')
bth4 = tk.Button(win, text= 'Hello 4')
bth5 = tk.Button(win, text= 'Hello 5')
bth6 = tk.Button(win, text= 'Hello 6')
bth7 = tk.Button(win, text= 'Hello 7')
bth8 = tk.Button(win, text= 'Hello 8')

bth1.grid(row=0, column=0)
bth2.grid(row=0, column=1)
bth3.grid(row=1, column=0)
bth4.grid(row=1, column=1)
bth5.grid(row=2, column=0)
bth6.grid(row=2, column=1)

# columnspan смешает её на середину а stick расстягивает их по ширине
bth7.grid(row=3, column=0, columnspan=2, stick='we')

bth8.grid(row=0, column=2, rowspan=4, stick='ns')
win.mainloop()