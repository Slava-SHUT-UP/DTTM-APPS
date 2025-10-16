from tkinter import *
from tkinter import ttk

root = Tk()

file_name_name = "Безымянный"
current_font_size = 11
current_theme = 'clam'

style = ttk.Style()
style.theme_use(current_theme)


def about():
    about_window = Toplevel(root)
    about_window.title("О Текстовом редакторе")
    about_window.geometry("400x200")
    about_window.resizable(False, False)

    about_window.transient(root)
    about_window.grab_set()

    bio = ttk.Label(about_window,
                    text="2025 DTTM\nОткрытый Текстовый редактор, каждый может внести туда вклад\nВсё ради вашего Удобства!",
                    justify=CENTER,
                    padding=20)
    bio.pack(pady=10)

    ok_button = ttk.Button(about_window,
                           text="OK",
                           command=about_window.destroy)
    ok_button.pack(pady=10)

    about_window.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - about_window.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - about_window.winfo_height()) // 2
    about_window.geometry(f"+{x}+{y}")


def theme():
    theme_window = Toplevel(root)
    theme_window.title("Выбрать тему")
    theme_window.geometry("300x300")
    theme_window.resizable(False, False)
    theme_window.transient(root)
    theme_window.grab_set()

    themes = list(style.theme_names())

    theme_label = ttk.Label(theme_window, text="Выберите тему:")
    theme_label.pack(pady=10)

    theme_var = StringVar(value=current_theme)

    for theme_name in themes:
        rb = ttk.Radiobutton(theme_window,
                             text=theme_name,
                             variable=theme_var,
                             value=theme_name)
        rb.pack(anchor='w', padx=20)

    def apply_theme():
        global current_theme
        current_theme = theme_var.get()
        style.theme_use(current_theme)
        theme_window.destroy()
        update_status_bar(f"Тема изменена на: {current_theme}")

    apply_btn = ttk.Button(theme_window,
                           text="Применить",
                           command=apply_theme)
    apply_btn.pack(pady=10)

    cancel_btn = ttk.Button(theme_window,
                            text="Отмена",
                            command=theme_window.destroy)
    cancel_btn.pack(pady=5)


def sizeFont():
    font_window = Toplevel(root)
    font_window.title("Размер шрифта")
    font_window.geometry("300x300")
    font_window.resizable(False, False)
    font_window.transient(root)
    font_window.grab_set()

    size_label = ttk.Label(font_window, text="Выберите размер шрифта:")
    size_label.pack(pady=10)

    size_var = IntVar(value=current_font_size)

    sizes = [8, 10, 11, 12, 14, 16, 18, 20, 24]

    for size in sizes:
        rb = ttk.Radiobutton(font_window,
                             text=f"{size} pt",
                             variable=size_var,
                             value=size)
        rb.pack(anchor='w', padx=20)

    def apply_font_size():
        global current_font_size
        current_font_size = size_var.get()
        txt.config(font=('Arial', current_font_size))
        font_window.destroy()
        update_status_bar(f"Размер шрифта изменен на: {current_font_size}")

    apply_btn = ttk.Button(font_window,
                           text="Применить",
                           command=apply_font_size)
    apply_btn.pack(pady=10)

    cancel_btn = ttk.Button(font_window,
                            text="Отмена",
                            command=font_window.destroy)
    cancel_btn.pack(pady=5)


def new_file():
    txt.delete(1.0, END)
    global file_name_name
    file_name_name = "Безымянный"
    root.title(f"DTTMTextEditor - {file_name_name}")
    update_status_bar("Создан новый файл")


def open_file():
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                txt.delete(1.0, END)
                txt.insert(1.0, content)
            global file_name_name
            file_name_name = file_path.split('/')[-1]
            root.title(f"DTTMTextEditor - {file_name_name}")
            update_status_bar(f"Файл открыт: {file_name_name}")
        except Exception as e:
            update_status_bar(f"Ошибка открытия файла: {str(e)}")


def save_file():
    from tkinter import filedialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                content = txt.get(1.0, END)
                file.write(content)
            global file_name_name
            file_name_name = file_path.split('/')[-1]
            root.title(f"DTTMTextEditor - {file_name_name}")
            update_status_bar(f"Файл сохранен: {file_name_name}")
        except Exception as e:
            update_status_bar(f"Ошибка сохранения файла: {str(e)}")


def update_status_bar(message):
    status_bar.config(text=message)


def on_text_change(event=None):
    update_status_bar("Редактирование...")


root.title(f"DTTMTextEditor - {file_name_name}")
root.geometry('800x600')

try:
    icon = PhotoImage(file="ico.png")
    root.iconphoto(True, icon)
except:
    print("Иконка не найдена, используется стандартная")

menu = Menu(root)

file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label='Новый', command=new_file)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_command(label='Сохранить', command=save_file)
menu.add_cascade(label='Файл', menu=file_menu)

settings_menu = Menu(menu, tearoff=0)
settings_menu.add_command(label='Поменять тему', command=theme)
settings_menu.add_command(label='Изменить размер шрифта', command=sizeFont)
settings_menu.add_command(label='Выход', command=lambda: root.destroy())
menu.add_cascade(label='Настройки', menu=settings_menu)

help_menu = Menu(menu, tearoff=0)
help_menu.add_command(label='О программе', command=about)
menu.add_cascade(label='Помощь', menu=help_menu)

root.config(menu=menu)

main_frame = ttk.Frame(root)
main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

scrollbar = ttk.Scrollbar(main_frame)
scrollbar.pack(side=RIGHT, fill=Y)

txt = Text(main_frame,
           yscrollcommand=scrollbar.set,
           font=('Arial', current_font_size),
           wrap=WORD,
           padx=10,
           pady=10)
txt.pack(fill=BOTH, expand=True)

scrollbar.config(command=txt.yview)

txt.bind('<KeyPress>', on_text_change)

status_bar = ttk.Label(root, text="Готов", relief=SUNKEN, anchor=W)
status_bar.pack(side=BOTTOM, fill=X)

root.mainloop()
