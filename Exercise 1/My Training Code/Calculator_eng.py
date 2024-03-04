import tkinter as tk
from tkinter import messagebox

# These comments are just for myself. To remember how functions work

# row=0, column=1 || row - row || column - column
# sticky=tk.W || stick to the west, i.e., left
# sticky=tk.E || stick to the east, i.e., right
# sticky=tk.CENTER || stick to the center
# sticky='we' || from west to east, i.e., stretch from left to right
# sticky='wens' || stretch in all four directions
# padx=10 || shift to the right || pady=10 || shift down

# Function responsible for buttons from 0 to 9
def make_digit_button(digit):
    return tk.Button(win, text=digit, bd=5, font=('Arial', 10), command=lambda: add_digit(digit))

# Function responsible for buttons + - * /
def make_operation_button(operation):
    return tk.Button(win, text=operation, bd=5, font=('Arial', 13), fg='#11d911', bg='#D3D3D3', command=lambda: add_operation(operation))

# Function responsible for the = button
def make_calc_button(operation):
    return tk.Button(win, text=operation, bd=5, font=('Arial', 13), fg='#ffffff', bg='#11d911', command=calculate)

# Function responsible for the C button
def make_clear_button(operation):
    return tk.Button(win, text=operation, bd=5, font=('Arial', 13), fg='#fb2c03', bg='#939393', command=clear)

def add_digit(digit):

    value = calc.get()

    # If the first character is '0' and the length of the string is 1, remove '0' and add a new digit
    if value[0] == '0' and len(value) == 1:
        value = value[1:]

    # Clear the input field and add the new digit
    calc.delete(0, tk.END)
    calc.insert(0, value + digit)

def add_keyboard_digit(event):
    value = calc.get()
    if value[0] == '0' and len(value) == 1:
        calc.delete(0, tk.END)

def add_operation(operation):

    value = calc.get()

    if value[-1] in '+-/*':
        value = value[:-1]
    calc.delete(0, tk.END)
    calc.insert(0, value + operation)

def calculate():
    # Accept values in the input
    value = calc.get()
    # Remove all spaces from the string.
    value = value.replace(' ', '')

    # If the user enters, for example, 15+ and then =, the calculator will compute it as 15+15=30
    if value[-1] in '+-/*':
        value = value+value[:-1]

    # This code splits the string by '/', then checks if the last element after the split is '0'. If yes, it displays an error message about division by zero.
    if '/' in value:
        parts = value.split('/')
        if len(parts) > 1 and parts[-1] == '0':
            messagebox.showerror("Error", "Division by zero!")
            return

    # Check if the string consists only of digits or allowed special characters
    if all(char.isdigit() or char in '+-*/.' for char in value):
        # Clear the input field
        calc.delete(0, tk.END)
        # Calculate and display the result
        calc.insert(0, eval(value))
    else:
        # Show an error message
        messagebox.showerror("Error", "Invalid expression!")
        # Exit the function
        return

def clear():
    calc.delete(0, tk.END)
    calc.insert(0, '0')

# Create the graphical window
win = tk.Tk()
# Rename the program
win.title('Calculator')
# Set the default size
win.geometry(f'238x265+100+200')
# Prevent resizing the window
win.resizable(width=False, height=False)
# Set the background color
win['bg'] = 'black'
# Replace the default icon
photo = tk.PhotoImage(file='calculator.png')
win.iconphoto(False, photo)

# Input field || justify=tk.LEFT - aligns text to the left
calc = tk.Entry(win, justify=tk.LEFT, font=('Arial', 15), width=15)

# Set '0' in the input field when the calculator starts
calc.insert(0, '0')

# Place the input field on the main window
calc.grid(row=0, column=0, columnspan=4, stick='we')

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

# When Enter is pressed in the input field, calculate the result without pressing the '=' button
win.bind('<Return>', lambda event: calculate())

# To remove '0' from the input field by default when typing from 0 to 9 on the keyboard
calc.bind('1', add_keyboard_digit)
calc.bind('2', add_keyboard_digit)
calc.bind('3', add_keyboard_digit)
calc.bind('4', add_keyboard_digit)
calc.bind('5', add_keyboard_digit)
calc.bind('6', add_keyboard_digit)
calc.bind('7', add_keyboard_digit)
calc.bind('8', add_keyboard_digit)
calc.bind('9', add_keyboard_digit)
calc.bind('0', add_keyboard_digit)

# To clear the input field when pressing the 'C' key on the keyboard
win.bind('c', lambda event: clear())
win.bind('C', lambda event: clear())

# Set minimum column widths so they don't compress too much when the user resizes the window or when widgets are placed in them.
# They also affect the size of buttons at the right end.
win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=60)

# Rows won't compress vertically to less than 60 pixels, even if they are empty or the user resizes the window.
win.grid_rowconfigure(1, minsize=60)
win.grid_rowconfigure(2, minsize=60)
win.grid_rowconfigure(3, minsize=60)
win.grid_rowconfigure(4, minsize=60)

# Run the application
win.mainloop()
