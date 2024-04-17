import tkinter as tk

def button_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

def button_clear():
    global expression
    expression = ""
    input_text.set("")

def button_equal():
    try:
        global expression
        result = str(eval(expression)) # виконує обчислення введеного виразу
        input_text.set(result)
        expression = result  # Зберігаємо результат, щоб його можна було використати для нових обчислень
    except:
        input_text.set("Помилка")
        expression = ""

expression = ""

# Створення вікна
root = tk.Tk()
root.title("Калькулятор")

# Поле для вводу
input_text = tk.StringVar()
input_field = tk.Entry(root, textvariable=input_text)
input_field.grid(row=0, columnspan=4)

# Кнопки
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row_index = 1
col_index = 0

for button in buttons:
    if button == '=':
        tk.Button(root, text=button, width=5, command=button_equal).grid(row=row_index, column=col_index)
    elif button == 'C':
        tk.Button(root, text=button, width=5, command=button_clear).grid(row=row_index, column=col_index)
    else:
        tk.Button(root, text=button, width=5, command=lambda item=button: button_click(item)).grid(row=row_index, column=col_index)
    col_index += 1
    if col_index > 3:
        col_index = 0
        row_index += 1

# Запуск головного циклу
root.mainloop()
