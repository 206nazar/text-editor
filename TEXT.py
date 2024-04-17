from tkinter import *
from tkinter import messagebox, filedialog, simpledialog, font as tk_font
from tkinter.colorchooser import askcolor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import pyautogui
from subprocess import Popen


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title('Текстовий редактор')
        self.root.geometry('800x600')

        self.status_bar = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)


        self.current_theme = 'light'
        self.current_font = 'Arial'
        self.current_font_size = 14

        # Лінія з кнопками
        button_frame = Frame(root, relief=RAISED, bd=1)
        button_frame.pack(side=TOP, fill=X)

        # Кнопки для стилю
        button_bold = Button(button_frame, text="Жирний", command=self.bold_text)
        button_bold.pack(side=LEFT, padx=5)

        button_italic = Button(button_frame, text="Похилий", command=self.italic_text)
        button_italic.pack(side=LEFT, padx=5)

        button_strike = Button(button_frame, text="Закреслений", command=self.strike_text)
        button_strike.pack(side=LEFT, padx=5)

        button_color = Button(button_frame, text="Змінити колір", command=self.change_text_color)
        button_color.pack(side=LEFT, padx=5)

        button_bullet = Button(button_frame, text="Маркований список", command=self.insert_bullet_list)
        button_bullet.pack(side=LEFT, padx=5)

        button_numbered = Button(button_frame, text="Нумерований список", command=self.insert_numbered_list)
        button_numbered.pack(side=LEFT, padx=5)

        button_table = Button(button_frame, text="Реалістична таблиця", command=self.insert_custom_realistic_table)
        button_table.pack(side=LEFT, padx=5)

        button_search = Button(button_frame, text="Пошук і заміна", command=self.search_and_replace)
        button_search.pack(side=LEFT, padx=5)

        # Кнопки для вигляду
        button_theme_dark = Button(button_frame, text="Темна тема", command=lambda: self.change_theme('dark'))
        button_theme_dark.pack(side=RIGHT, padx=5)

        button_theme_light = Button(button_frame, text="Світла тема", command=lambda: self.change_theme('light'))
        button_theme_light.pack(side=RIGHT, padx=5)

        button_font = Button(button_frame, text="Змінити шрифт", command=self.change_font)
        button_font.pack(side=RIGHT, padx=5)

        button_font_size = Button(button_frame, text="Змінити розмір шрифту", command=self.change_font_size)
        button_font_size.pack(side=RIGHT, padx=5)

        button_game = Button(button_frame, text="Гра", command=self.launch_game)
        button_game.pack(side=LEFT, padx=5)

        button_calculator = Button(button_frame, text="Калькулятор", command=self.open_calculator)
        button_calculator.pack(side=LEFT, padx=5)

        # Текстове поле з прокруткою
        self.text_field = Text(root, bg='white', fg='black', padx=10, pady=10, wrap=WORD, insertbackground='black', font=(self.current_font, self.current_font_size))
        self.text_field.pack(side=LEFT, fill=BOTH, expand=1)

        self.scroll = Scrollbar(root)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.text_field.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.text_field.yview)

        # Головне меню
        main_menu = Menu(root)

        # Файл
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Відкрити', command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label='Зберегти', command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Зберегти у PDF', command=self.save_as_pdf)
        file_menu.add_separator()
        file_menu.add_command(label='Новий файл', command=self.new_file)
        file_menu.add_separator()
        file_menu.add_command(label='Вихід', command=self.notepad_exit)
        main_menu.add_cascade(label='Файл', menu=file_menu)

        # Вигляд
        view_menu = Menu(main_menu, tearoff=0)
        view_menu.add_command(label='Темна тема', command=lambda: self.change_theme('dark'))
        view_menu.add_command(label='Світла тема', command=lambda: self.change_theme('light'))
        view_menu.add_command(label='Змінити шрифт', command=self.change_font)
        view_menu.add_command(label='Змінити розмір шрифту', command=self.change_font_size)

        root.config(menu=main_menu)

        self.setup_shortcuts()  # Додати гарячі клавіші

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Текстові файли", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_field.delete(1.0, END)
                self.text_field.insert(1.0, content)

    def open_calculator(self):
        try:
            # Отримання шляху до директорії поточного файлу
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Запуск файлу calculator.py
            Popen(["python", os.path.join(current_dir, "calculator.py")])
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка запуску калькулятора: {e}")

    def launch_game(self):
        try:
            # Отримання шляху до директорії поточного файлу
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Запуск файлу main.py
            Popen(["python", os.path.join(current_dir, "game.py")])
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка запуску гри: {e}")

    def new_file(self):
        self.text_field.delete(1.0, END)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстові файли", "*.txt")])
        if file_path:
            content = self.text_field.get(1.0, END)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

    def save_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            content = self.text_field.get(1.0, END)
            pdf = canvas.Canvas(file_path, pagesize=letter)
            pdf.drawString(100, 750, content)
            pdf.save()

    def notepad_exit(self):
        answer = messagebox.askokcancel('Вихід', 'Ви впевнені, що хочете вийти?')
        if answer:
            self.root.destroy()

    def change_theme(self, theme):
        view_colors = {
            'dark': {'text_bg': 'black', 'text_fg': 'lime', 'cursor': 'brown'},
            'light': {'text_bg': 'white', 'text_fg': 'black', 'cursor': 'black'}
        }
        self.text_field.config(bg=view_colors[theme]['text_bg'], fg=view_colors[theme]['text_fg'],
                                insertbackground=view_colors[theme]['cursor'])

    def setup_shortcuts(self):
        self.root.bind('<Control-b>', lambda event: self.bold_text())  # Ctrl+B для жирного
        self.root.bind('<Control-i>', lambda event: self.italic_text())  # Ctrl+I для похиленого
        self.root.bind('<Control-Shift-s>', lambda event: self.strike_text())  # Ctrl+Shift+S для закресленого
        self.root.bind('<Control-l>', lambda event: self.insert_bullet_list())  # Ctrl+L для маркованого списку
        self.root.bind('<Control-n>', lambda event: self.insert_numbered_list())  # Ctrl+N для нумерованого списку
        self.root.bind('<Control-f>', lambda event: self.search_and_replace())  # Ctrl+F для пошуку і заміни
        self.root.bind('<Control-o>', lambda event: self.open_file())  # Ctrl+O для відкриття файлу
        self.root.bind('<Control-s>', lambda event: self.save_file())  # Ctrl+S для збереження файлу
        self.root.bind('<Control-q>', lambda event: self.notepad_exit())  # Ctrl+Q для виходу
        self.root.bind('<Control-p>', lambda event: self.print_text())  # Ctrl+P для друку

    def print_text(self):
        pyautogui.hotkey('ctrl', 'p')  # Спрацьовує гаряча клавіша Ctrl+P для виклику діалогу друку

    def insert_realistic_table(self, rows, columns):
        self.table_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(columns):
                entry = Entry(self.text_field, borderwidth=1, relief="solid")
                entry.grid(row=i, column=j, sticky="nsew")
                row_entries.append(entry)
            self.table_entries.append(row_entries)
        for i in range(rows):
            self.text_field.grid_rowconfigure(i, weight=1)
        for j in range(columns):
            self.text_field.grid_columnconfigure(j, weight=1)

    def insert_custom_realistic_table(self):
        rows = simpledialog.askinteger("Створення таблиці", "Введіть кількість рядків:")
        columns = simpledialog.askinteger("Створення таблиці", "Введіть кількість стовпців:")
        if rows and columns:
            self.insert_realistic_table(rows, columns)

    def change_font(self):
        font_name = simpledialog.askstring("Зміна шрифту", "Введіть назву шрифту:")
        if font_name:
            self.current_font = font_name
            self.text_field.config(font=(font_name, self.current_font_size))

    def change_font_size(self):
        font_size = simpledialog.askinteger("Зміна розміру шрифту", "Введіть розмір шрифту:")
        if font_size:
            self.current_font_size = font_size
            self.text_field.config(font=(self.current_font, font_size))

    def bold_text(self):
        try:
            if self.text_field.tag_ranges("sel"):
                current_tags = self.text_field.tag_names("sel.first")
                if "bold" in current_tags:
                    self.text_field.tag_remove("bold", "sel.first", "sel.last")
                else:
                    self.text_field.tag_add("bold", "sel.first", "sel.last")
                    self.text_field.tag_configure("bold", font=(self.current_font, self.current_font_size, "bold"))
        except:
            pass

    def italic_text(self):
        try:
            if self.text_field.tag_ranges("sel"):
                current_tags = self.text_field.tag_names("sel.first")
                if "italic" in current_tags:
                    self.text_field.tag_remove("italic", "sel.first", "sel.last")
                else:
                    self.text_field.tag_add("italic", "sel.first", "sel.last")
                    self.text_field.tag_configure("italic", font=(self.current_font, self.current_font_size, "italic"))
        except:
            pass

    def strike_text(self):
        try:
            if self.text_field.tag_ranges("sel"):
                current_tags = self.text_field.tag_names("sel.first")
                if "strike" in current_tags:
                    self.text_field.tag_remove("strike", "sel.first", "sel.last")
                else:
                    self.text_field.tag_add("strike", "sel.first", "sel.last")
                    self.text_field.tag_configure("strike", font=(self.current_font, self.current_font_size, "overstrike"))
        except:
            pass

    def change_text_color(self):
        try:
            if self.text_field.tag_ranges("sel"):
                color = askcolor(title="Виберіть колір тексту")[1]
                if color:
                    start_index = self.text_field.index("sel.first")
                    end_index = self.text_field.index("sel.last")
                    tag_name = f"colored_{start_index}_{end_index}"
                    self.text_field.tag_add(tag_name, start_index, end_index)
                    self.text_field.tag_configure(tag_name, foreground=color)
        except Exception as e:
            print("Error changing text color:", e)

    def insert_bullet_list(self):
        try:
            if self.text_field.tag_ranges("sel"):
                start_index = self.text_field.index("sel.first")
                end_index = self.text_field.index("sel.last")
                lines = self.text_field.get(start_index, end_index).split("\n")
                formatted_lines = "\n".join([f"• {line}" for line in lines])
                self.text_field.delete(start_index, end_index)
                self.text_field.insert(start_index, formatted_lines)
        except Exception as e:
            print("Error inserting bullet list:", e)

    def insert_numbered_list(self):
        try:
            if self.text_field.tag_ranges("sel"):
                start_index = self.text_field.index("sel.first")
                end_index = self.text_field.index("sel.last")
                lines = self.text_field.get(start_index, end_index).split("\n")
                formatted_lines = "\n".join([f"{i + 1}. {line}" for i, line in enumerate(lines)])
                self.text_field.delete(start_index, end_index)
                self.text_field.insert(start_index, formatted_lines)
        except Exception as e:
            print("Error inserting numbered list:", e)

    def search_and_replace(self):
        try:
            if self.text_field.tag_ranges("sel"):
                find_str = simpledialog.askstring("Пошук і заміна", "Введіть текст для пошуку:")
                if find_str:
                    replace_str = simpledialog.askstring("Пошук і заміна", "Введіть текст для заміни:")
                    if replace_str:
                        content = self.text_field.get(1.0, END)
                        updated_content = content.replace(find_str, replace_str)
                        self.text_field.delete(1.0, END)
                        self.text_field.insert(1.0, updated_content)
        except:
            pass

# Створення вікна
root = Tk()
editor = TextEditor(root)
editor.setup_shortcuts()  # Додати гарячі клавіші
root.mainloop()
