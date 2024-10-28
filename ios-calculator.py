import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg='#1C1C1C')
        
        # Calculator state
        self.current = "0"
        self.new_number = True
        self.op_pending = None
        self.last_operation = None
        self.last_number = None

        # Display
        self.display_var = tk.StringVar(value=self.current)
        display = tk.Label(
            root,
            textvariable=self.display_var,
            anchor='e',
            bg='#1C1C1C',
            fg='white',
            font=('Arial', 40),
            padx=10,
            pady=10
        )
        display.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # Button layout
        buttons = [
            ('AC', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        # Create buttons
        for button in buttons:
            if len(button) == 4:  # For zero button that spans two columns
                text, row, col, colspan = button
                width = 160
            else:
                text, row, col = button
                colspan = 1
                width = 80

            btn = tk.Button(
                root,
                text=text,
                width=2,
                height=1,
                font=('Arial', 20),
                bd=0,
                padx=20,
                pady=20
            )
            
            # Style buttons
            if text in ['÷', '×', '-', '+', '=']:
                btn.configure(bg='#FF9F0A', fg='white')
            elif text in ['AC', '±', '%']:
                btn.configure(bg='#A5A5A5', fg='black')
            else:
                btn.configure(bg='#333333', fg='white')

            # Bind button commands
            if text.isdigit() or text == '.':
                btn.configure(command=lambda t=text: self.number_press(t))
            elif text in ['÷', '×', '-', '+']:
                btn.configure(command=lambda t=text: self.operation(t))
            elif text == '=':
                btn.configure(command=self.calculate)
            elif text == 'AC':
                btn.configure(command=self.clear)
            elif text == '±':
                btn.configure(command=self.toggle_sign)
            elif text == '%':
                btn.configure(command=self.percentage)

            btn.grid(row=row, column=col, columnspan=colspan, padx=1, pady=1, sticky='nsew')

        # Configure grid
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def number_press(self, num):
        if self.new_number:
            self.current = num
            self.new_number = False
        else:
            if num == '.' and '.' in self.current:
                return
            self.current = self.current + num
        self.update_display()

    def operation(self, op):
        if self.op_pending:
            self.calculate()
        self.op_pending = op
        self.last_number = float(self.current)
        self.new_number = True

    def calculate(self):
        if self.op_pending:
            current = float(self.current)
            if self.op_pending == '+':
                result = self.last_number + current
            elif self.op_pending == '-':
                result = self.last_number - current
            elif self.op_pending == '×':
                result = self.last_number * current
            elif self.op_pending == '÷':
                if current == 0:
                    result = "Error"
                else:
                    result = self.last_number / current
            
            if result == "Error":
                self.current = result
            else:
                self.current = str(result) if result % 1 else str(int(result))
            
            self.new_number = True
            self.op_pending = None
            self.update_display()

    def clear(self):
        self.current = "0"
        self.new_number = True
        self.op_pending = None
        self.last_operation = None
        self.last_number = None
        self.update_display()

    def toggle_sign(self):
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.update_display()

    def percentage(self):
        if self.current:
            current = float(self.current)
            self.current = str(current / 100)
            self.update_display()

    def update_display(self):
        self.display_var.set(self.current)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("320x500")
    calculator = Calculator(root)
    root.mainloop()
