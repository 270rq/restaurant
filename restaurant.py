from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

root = Tk()
root.title('Ресторан')

def get_rgb(rgb):
    return "#%02x%02x%02x" % rgb 

style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background=get_rgb((118, 227, 131)), foreground="black")
style.map('Treeview', background=[('selected', get_rgb((73, 140,81)))])
def clear_root():
    for widget in root.winfo_children():
        widget.destroy()
    show_menu(role=user_role)
def show_employ():
    clear_root()
    employ_frame = LabelFrame(root, text='Сотрудники').pack(pady=10)

    employ_scroll = Scrollbar(employ_frame)
    employ_scroll.pack(side=RIGHT, fill=Y)

    employ_tree = ttk.Treeview(employ_frame, yscrollcommand=employ_scroll.set, selectmode='extended')
    employ_tree.pack()

    employ_scroll.config(command=employ_tree.yview)
    employ_tree['columns'] = ('ID', 'Name','Password', 'Role', 'Status')
    employ_tree.column('#0', width=0, anchor=W)
    employ_tree.column('ID', width=50, anchor=CENTER)
    employ_tree.column('Name', width=120, anchor=CENTER)
    employ_tree.column('Role', width=120, anchor=CENTER)
    employ_tree.column('Status', width=120, anchor=CENTER)

    employ_tree.heading('#0', text='', anchor=W)
    employ_tree.heading('ID', text='ID', anchor=CENTER)
    employ_tree.heading('Name', text='Имя', anchor=CENTER)
    employ_tree.heading('Password', text='Пароль', anchor=CENTER)
    employ_tree.heading('Role', text='Роль', anchor=CENTER)
    employ_tree.heading('Status', text='Статус', anchor=CENTER)

    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()

    for row in records:
        employ_tree.insert('', 'end', values=row)

    employ_tree.bind(show_selected_item_employ)

    employ_data_frame = LabelFrame(root, text='Данные сотрудника')
    employ_data_frame.pack(padx=20)

    name_label = Label(employ_data_frame, text="Имя").grid(row=1, column=0, padx=10, pady=10)
    name_entry = Entry(employ_data_frame).grid(row=1, column=1, padx=10, pady=10)

    role_label = Label(employ_data_frame, text="Роль").grid(row=1, column=2, padx=10, pady=10)
    role_combobox = ttk.Combobox(employ_data_frame, values=['Повар', 'Официант'], state='readonlбy').grid(row=1, column=3, padx=10, pady=10)

    password_label = Label(employ_data_frame, text="Пароль").grid(row=1, column=4, padx=10, pady=10)
    password_entry = Entry(employ_data_frame).grid(row=1, column=5, padx=10, pady=10)

    status_label = Label(employ_data_frame, text="Статус").grid(row=1, column=6, padx=10, pady=10)
    status_combobox = ttk.Combobox(employ_data_frame, values=['Активен','Уволен'], state='readonly').grid(row=1, column=7, padx=10, pady=10)

    employ_action_frame = LabelFrame(root, text='Команды')
    employ_action_frame.pack(fill='x', expand='yes', padx=20)

    add_employee_button = Button(employ_action_frame, text="Добавить", command=lambda: add_employ(name_e)).grid(row=0, column=0, padx=10, pady=10)
    update_employee_button = Button(employ_action_frame, text="Обновить", command=update_employ).grid(row=0, column=1, padx=10, pady=10)

def show_shift():
    clear_root()
    
    shift_frame = LabelFrame(root, text='Смены').pack(pady=10)

    shift_scroll = Scrollbar(shift_frame).pack(side='right', fill='y')
    shift_tree = ttk.Treeview(shift_frame, yscrollcommand=shift_scroll, selectmode='extended').pack()
    shift_scroll.config(command=shift_tree.yview)

    shift_tree['columns'] = ('ID', 'employees')
    shift_tree.column('#0', width=0, anchor=W)
    shift_tree.column('ID', width=10, anchor=W)
    shift_tree.column('employees', width=100, anchor=CENTER)

    shift_tree.heading('#0', text='', anchor=W)
    shift_tree.heading('ID', text='ID', anchor=W)
    shift_tree.heading('employees', text='Сотрудники', anchor=CENTER)

    cursor.execute('SELECT * FROM shift')
    records = cursor.fetchall()
    for row in records:
        shift_tree.insert('', 'end', values=row)
        

    data_shift_frame = LabelFrame(root, text="Данные смены")
    data_shift_frame.pack(padx=10, pady=10, fill='both')

    def get_active_employees():
        cursor.execute("SELECT name FROM users WHERE status = 'Активен'")
        active_employees = [row[0] for row in cursor.fetchall()]
        return active_employees

    employ_list = Listbox(data_shift_frame).grid(row=0, column=3, padx=5, pady=5)
    active_employees = get_active_employees()

    for employee in active_employees:
        employ_list.insert(END, employee)

    id_label = Label(data_shift_frame, text='Номер смены').grid(row=0, column=0, padx=5, pady=5)
    id_entry = Entry(data_shift_frame).grid(row=0, column=1, padx=5, pady=5)
    employ_label = Label(data_shift_frame, text='Сотрудники').grid(row=0, column=2, padx=5, pady=5)

    action_frame = LabelFrame(root, text="Действия").pack(padx=10, pady=20, fill='both')

    add_button = Button(action_frame, text='Добавить', command=add_shift).grid(row=1, column=0, padx=0, pady=0)

    shift_tree.bind('<<TreeviewSelect>>', show_selected_item_shift)


def show_menu(role):
    def show_order():
        clear_root()
        order_frame = LabelFrame(root, text='Заказы')
        order_frame.pack(pady=10)

        order_scroll = Scrollbar(order_frame)
        order_scroll.pack(side=RIGHT, fill=Y)

        order_tree = ttk.Treeview(order_frame, yscrollcommand=order_scroll.set, selectmode='extended')
        order_tree.pack()

        order_tree['columns'] = ('ID', 'table', 'count', 'items', 'status', 'supervisor')
        order_tree.column('#0', width=0, anchor=W)
        order_tree.column('ID', width=50, anchor=W)
        order_tree.column('table', width=50, anchor=CENTER)
        order_tree.column('items', width=50, anchor=CENTER)
        order_tree.column('status', width=50, anchor=CENTER)
        order_tree.column('supervisor', width=50, anchor=CENTER)

        order_tree.heading('#0', text='', anchor=W)
        order_tree.heading('ID', text='ID', anchor=W)
        order_tree.heading('table', text='Номер столика', anchor=CENTER)
        order_tree.heading('count', text='Количество гостей', anchor=CENTER)
        order_tree.heading('items', text='Список заказа', anchor=CENTER)
        order_tree.heading('supervisor', text='Сотрудник', anchor=CENTER)
        order_tree.heading('status', text='Статус заказа', anchor=CENTER)

        order_scroll.config(command=order_tree.yview)

        cursor.execute('SELECT * FROM orders')
        records = cursor.fetchall()

        for row in records:
            order_tree.insert('', 'end', values=row)

        order_data_frame = LabelFrame(root, text='Данные о заказе')
        order_data_frame.pack(padx=20, pady=10, fill='both')
        action_order_frame = LabelFrame(root, text='Команды')
        action_order_frame.pack(pady=10)
        

        if user_role=='Повар':
            table_entry = Entry(order_data_frame, state='readonly')
            count_entry = Entry(order_data_frame, state='readonly')
            item_entry = Entry(order_data_frame, state='readonly')
            table_entry.grid(row=0, column=1, padx=5, pady=5)
            add_order_button = Button(action_order_frame, state='disabled')
            update_order_button = Button(action_order_frame)
            status_order = ttk.Combobox(order_data_frame, values=('Готов','Готовится'), state='readonly').grid(row=3, column=1, padx=5, pady=5)
        elif user_role=='Официант':
            table_entry = Entry(order_data_frame)
            count_entry = Entry(order_data_frame)
            item_entry = Entry(order_data_frame)
            add_order_button = Button(order_data_frame)
            table_entry.grid(row=0, column=1, padx=5, pady=5)
            status_order = ttk.Combobox(order_data_frame, values=['Принят','Оплачен'], state='readonly').grid(row=3, column=1, padx=5, pady=5)
            add_order_button = Button(action_order_frame)
            update_order_button = Button(action_order_frame)
        elif user_role=='Администратор':
            order_data_frame.grid_remove()
            action_order_frame.grid_remove()

        order_tree.bind(show_selected_item_order)
    
        table_label = Label(order_data_frame, text='Номер столика').grid(row=0, column=0, padx=5, pady=5)

        count_label = Label(order_data_frame, text='Количество гостей').grid(row=0, column=2, padx=5, pady=5)
        count_entry.grid(row=0, column=3, padx=5, pady=5)

        item_label = Label(order_data_frame, text='Список заказа').grid(row=1, column=0, padx=5, pady=5)
        item_entry.grid(row=1, column=1, padx=5, pady=5)

        user_label = Label(order_data_frame, text='Сотрудник').grid(row=1, column=2, padx=5, pady=5)
        user_entry.grid(row=1, column=3, padx=5, pady=5)

        status_label = Label(order_data_frame, text='Статус заказа').grid(row=2, column=0, padx=5, pady=5)
        status_entry.grid(row=2, column=0, padx=5, pady=5)

        add_order_button = Button(action_order_frame, text='Добавить'). grid(row=3, column=0, padx=5, pady=5)
        update_order_button = Button(action_order_frame, text='Обновить').grid(row=4, column=0, padx=5, pady=5)

    main_menu = Menu(root)
    inf_menu = Menu(main_menu, tearoff=0)
    if role == 'Администратор':
        inf_menu.add_command(label='Сотрудники', command=show_employ)
        inf_menu.add_command(label='Смены', command=show_shift)
    inf_menu.add_command(label="Заказы", command=show_order)

    inf_menu.add_separator()
    inf_menu.add_cascade(label='Выход')
    main_menu.add_cascade(label='Меню', menu=inf_menu)
    root.config(menu=main_menu)
    


def show_login_window():
    auth_frame = LabelFrame(root, text='Авторизация')
    auth_frame.pack(padx=50, pady=50)

    login_label = Label(auth_frame, text='Логин')
    login_label.grid(row=0, column=0)
    password_label = Label(auth_frame, text='Пароль')
    password_label.grid(row=1, column=0)

    login_var = Entry(auth_frame)
    login_var.grid(row=0, column=1)
    password_var = Entry(auth_frame)
    password_var.grid(row=1, column=1)
    

    def auth():
        global user_role
    
        login = login_var.get()
        password = password_var.get()
        if len(login) == 0 or len(password) == 0:
            messagebox.showerror("Ошибка", "Поля должны быть заполнены!")
        else:
            if login == "admin" and password == "admin":
                messagebox.showinfo('Успешная авторизация', 'Добро пожаловать, администратор!')
                auth_frame.pack_forget()
                user_role = 'Администратор'
                show_menu('Администратор')
            else:
                cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (login, password))
                user_role = cursor.fetchone()
                if user_role:
                    role = user_role[0]
                    messagebox.showinfo('Успешная авторизация', 'Добро пожаловать!')
                    auth_frame.pack_forget()
                    show_menu(role)
                else:
                    messagebox.showerror('Ошибка', 'Неверный логин или пароль')

    login_button = Button(auth_frame, text="Войти", command=auth)
    login_button.grid(row=2, columnspan=2)

show_login_window()

def show_selected_item_employ(employ_tree,event):
    name_entry.delete(0, END)
    password_entry.delete(0,END)
    role_combobox.delete(0,END)
    status_combobox.delete(0, END)
            
    selected = employ_tree.focus()
    item_values = employ_tree.item(selected,'values')
    name_entry.insert(0, item_values[1])
    password_entry.insert(0,item_values[2])
    role_combobox.set(item_values[3])
    status_combobox.set(item_values[4])

def show_selected_item_shift(event):
    selected_item = shift_tree.selection()
    if selected_item:
        item_values = shift_tree.item(selected_item)['values']
        if item_values:
            id_entry.delete(0, END)  
            id_entry.insert(0, item_values[0])
            employ_list.delete(0, END)
            employ_list.insert(END, item_values[1]) 
def show_selected_item_order(event):
    selected_item = order_tree.selection()
    if selected_item:
        item_values = order_tree.item(selected_item)['values']
        if item_values:
            table_entry.delete(0, END)
            table_entry.insert(0, item_values[0])
            count_entry.delete(0, END)
            count_entry.insert(0, item_values[1])
            item_entry.delete(0, END)
            item_entry.insert(0, item_values[2])
            user_entry.delete(0, END)
            user_entry.insert(0, item_values[3])
            status_entry.delete(0, END)
            status_entry.insert(0, item_values[4])
def add_employ(name,role,password,status):
    name = name_entry.get()
    role = role_combobox.get()
    password = password_entry.get()
    status = status_combobox.get()

    if not name or not role or not password or not status:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    try:
        cursor.execute("INSERT INTO users (username, role, password, status) VALUES (?, ?, ?, ?)", (name, role, password, status))
        conn.commit()
        employ_tree.insert('','end', values=(cursor.lastrowid, name, '',role,status))
        messagebox.showinfo('Сообщение','Данные удачно сохранены')
    except Exception as e:
        conn.rollback()
        messagebox.showinfo('Сообщение', 'Не удалось сохранить данные')
def add_shift():
    id = id_entry.get()
    employ = employ_list.get()

    if not id and not employ:
        messagebox.showerror('Ошибка', 'Заполните все поля')
        return
    try:
        cursor.execute("INSERT INTO shift (id, supervisor_id) VALUES (?, ?)", (id, employ))
        conn.commit()
        shift_tree.insert('','end', values = (cursor.lastrowid, id, employ))
        messagebox.showinfo('Сообщение','Данные удачно сохранены')
    except Exception as e:
        conn.rollback()
        messagebox.showinfo('Сообщение', 'Не удалось сохранить данные')
def update_employ():
    selected_item = employ_tree.focus()
    

    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите сотрудника для обновления")
        return

    name = name_entry.get()
    role = role_combobox.get()
    password = password_entry.get()
    status = status_combobox.get()

    if not name or not role or not password or not status:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    try:
        item_id = employ_tree.item(selected_item, "values")[0]

        cursor.execute("UPDATE users SET username=?, role=?, password=?, status=? WHERE id=?", (name, role, password, status, item_id))
        conn.commit()

        employ_tree.item(selected_item, text="", values=(item_id, name, '', role, status))
        messagebox.showinfo("Сообщение", "Данные обновлены!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Ошибка", f"Не удалось обновить данные: {str(e)}")
root.mainloop()
conn.close()