import tkinter as tk
from tkinter import messagebox
import sqlite3
from cryptography.fernet import Fernet
import re

class LoginRegisterApp:

    def __init__(self, root):
        # Initializing the login/registration application with the passed root (main) window
        self.root = root
        self.root.title("Login / Register")

        # Generating encryption key
        self.key = Fernet.generate_key()

        # Creating labels and entry fields for username and password input
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Adding a checkbox to show the password
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(root, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_checkbox.grid(row=1, column=2, padx=5)

        # Creating login and register buttons
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Creating the user database if it doesn't exist yet
        self.create_database()

    def toggle_password_visibility(self):
        # Function to toggle password visibility mode
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def create_database(self):
        # Creating the users table in the SQLite database if it doesn't exist yet
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
        # Method to handle user login
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Removing extra spaces from the username and password
        username = re.sub(r'\s+', ' ', username).strip()
        password = re.sub(r'^\s+|\s+$', '', password)

        if username.isdigit():
            messagebox.showerror("Error", "Username cannot consist only of digits!")
            return

        # Connecting to the database and executing the query
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Retrieving the user from the database by their username
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            # If the user is found, extract the encrypted password from the database
            stored_password = user[2]

            # Decrypting the encrypted password using the key
            cipher_suite = Fernet(self.key)
            decrypted_password = cipher_suite.decrypt(stored_password).decode()

            # Checking if the entered password matches the decrypted password from the database
            if password == decrypted_password:
                messagebox.showinfo("Success", "Login successful!")
                self.open_calculator()
            else:
                messagebox.showerror("Error", "Incorrect username or password!")
        else:
            messagebox.showerror("Error", "Incorrect username or password!")

        connection.close()

    def check_password(self, password, stored_password):
        # Method to check the user's password
        # Encrypting the entered password for comparison with the stored one
        cipher_suite = Fernet(Fernet.generate_key())
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password == stored_password

    def register(self):
        # Method to handle registration of a new user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Removing extra spaces from the username and password
        username = re.sub(r'\s+', ' ', username).strip()
        password = re.sub(r'^\s+|\s+$', '', password)

        if username.isdigit():
            messagebox.showerror("Error", "Username cannot consist only of digits!")
            return
        elif password.isdigit():
            messagebox.showerror("Error", "Password cannot consist only of digits!")
            return
        elif len(password) < 8:
            messagebox.showerror("Error", "Password must contain at least 8 characters!")
            return

        # Encrypting the password using the key
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode())

        # Connecting to the database and executing the query
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Inserting a new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
        connection.commit()
        connection.close()

        messagebox.showinfo("Registration", "Registration successful!")
        self.root.after(100, self.open_calculator)

    # Function to open the calculator window
    def open_calculator(self):
        # Close the login/registration window
        self.root.destroy()
        # Function to open the calculator window
        calc_win = tk.Tk()

        # Passing the calculator window to CalculatorApp
        app = CalculatorApp(calc_win)

        # Renaming the program
        calc_win.title("Calculator")

        # Setting the default size
        calc_win.geometry(f'238x265')
        # Preventing window resizing
        calc_win.resizable(width=False, height=False)
        # Setting the background color of the application
        calc_win['bg'] = 'black'

        # Main loop
        calc_win.mainloop()


class CalculatorApp(tk.Frame):

    def __init__(self, calc_win):
        super().__init__(calc_win)
        self.calc_win = calc_win

        # Input || justify=tk.LEFT - This property instructs the text to align to the left
        # width=15 || parameter specifies the number of characters that can be entered in the Entry field before it starts automatically wrapping text onto a new line
        self.calc = tk.Entry(calc_win, justify=tk.LEFT, font=('Arial', 15), width=15)

        # Setting '0' as the initial string when the calculator starts
        self.calc.insert(0, '0')

        # Placing the input field on the main window
        # Input field || The columnspan attribute merges multiple columns
        self.calc.grid(row=0, column=0, columnspan=4, sticky='we')

        # padx=5, pady=5 defines the distance between buttons
        # bd=5 defines the thickness of the borders || sticky='wens' || stretches the buttons
        self.make_digit_button('1').grid(row=1, column=0, sticky='wens', padx=5, pady=5)
        self.make_digit_button('2').grid(row=1, column=1, sticky='wens', padx=5, pady=5)
        self.make_digit_button('3').grid(row=1, column=2, sticky='wens', padx=5, pady=5)
        self.make_digit_button('4').grid(row=2, column=0, sticky='wens', padx=5, pady=5)
        self.make_digit_button('5').grid(row=2, column=1, sticky='wens', padx=5, pady=5)
        self.make_digit_button('6').grid(row=2, column=2, sticky='wens', padx=5, pady=5)
        self.make_digit_button('7').grid(row=3, column=0, sticky='wens', padx=5, pady=5)
        self.make_digit_button('8').grid(row=3, column=1, sticky='wens', padx=5, pady=5)
        self.make_digit_button('9').grid(row=3, column=2, sticky='wens', padx=5, pady=5)
        self.make_digit_button('0').grid(row=4, column=1, sticky='wens', padx=5, pady=5)

        self.make_operation_button('-').grid(row=4, column=0, sticky='wens', padx=5, pady=5)
        self.make_operation_button('+').grid(row=4, column=2, sticky='wens', padx=5, pady=5)

        self.make_clear_button('C').grid(row=1, column=3, sticky='wens', padx=5, pady=5)

        self.make_operation_button('/').grid(row=2, column=3, sticky='wens', padx=5, pady=5)
        self.make_operation_button('*').grid(row=3, column=3, sticky='wens', padx=5, pady=5)

        self.make_calc_button('=').grid(row=4, column=3, sticky='wens', padx=5, pady=5)

        # When Enter is pressed on the keyboard in the string, the calculator starts displaying the result without pressing the = button
        # `<Return>` indicates the Enter key on the keyboard
        self.calc_win.bind('<Return>', lambda event: self.calculate())

        # To clear the input field when typing from 0 to 9 digits on the keyboard
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

        # To clear the input field when pressing the C key on the keyboard
        self.calc_win.bind('c', lambda event: self.clear())
        self.calc_win.bind('C', lambda event: self.clear())

        # Setting minimum column widths to prevent them from compressing too much when the user resizes the window or when widgets are placed in them.
        # They also affect the size of the buttons on the right end
        self.calc_win.grid_columnconfigure(0, minsize=60)
        self.calc_win.grid_columnconfigure(1, minsize=60)
        self.calc_win.grid_columnconfigure(2, minsize=60)
        self.calc_win.grid_columnconfigure(3, minsize=60)

        # The grid row will not compress vertically to less than 60 pixels, even if it has no content or if the user resizes the window.
        self.calc_win.grid_rowconfigure(1, minsize=60)
        self.calc_win.grid_rowconfigure(2, minsize=60)
        self.calc_win.grid_rowconfigure(3, minsize=60)
        self.calc_win.grid_rowconfigure(4, minsize=60)


    def make_digit_button(self, digit):
        return tk.Button(self.calc_win, text=digit, bd=5, font=('Arial', 10), command=lambda: self.add_digit(digit))

    def add_digit(self, digit):

        value = self.calc.get()

        # If the first character is '0' and the length of the string is 1, remove '0' and add a new digit
        if value[0] == '0' and len(value) == 1:
            value = value[1:]

        # Clearing the input field and adding the new digit
        self.calc.delete(0, tk.END)
        self.calc.insert(0, value + digit)

    def add_keyboard_digit(self, event):
        value = self.calc.get()
        if value[0] == '0' and len(value) == 1:
            self.calc.delete(0, tk.END)

    def make_operation_button(self, operation):
        return tk.Button(self.calc_win, text=operation, bd=5, font=('Arial', 13), fg='#11d911', bg='#D3D3D3', command=lambda: self.add_operation(operation))

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
        # Accepting values in the input
        value = self.calc.get()
        # Removing all spaces from the string. The .strip() method doesn't fit here because it only removes leading and trailing spaces in a string, but doesn't remove spaces inside the string.
        value = value.replace(' ', '')

        # If the user enters, for example, 15+ and immediately activates =, the calculator will calculate it as 15+15=30
        if value[-1] in '+-/*':
            value = value + value[:-1]

        # This code splits the string by the '/' symbol, and then checks if the last element after the split is '0'. If yes, it displays an error message about division by zero.
        if '/' in value:
            parts = value.split('/')
            if len(parts) > 1 and parts[-1] == '0':
                messagebox.showerror("Error", "Division by zero!")
                return

        # Checking if the string consists only of digits or allowed special characters
        if all(char.isdigit() or char in '+-*/.' for char in value):
            # Clearing the input field
            self.calc.delete(0, tk.END)
            # Calculating and displaying the result || the eval function even reads the str string
            self.calc.insert(0, eval(value))
        else:
            # Displaying an error message
            messagebox.showerror("Error", "Invalid expression!")
            # Exiting the function
            return

def open_login_register():
    # Function to open the login/registration window
    login_register_window = tk.Tk()
    app = LoginRegisterApp(login_register_window)
    login_register_window.mainloop()

if __name__ == "__main__":
    open_login_register()
