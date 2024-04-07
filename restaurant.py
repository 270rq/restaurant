from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

root = Tk()
root.title('Ресторан')
root.geometry('600x600')
root.minsize('800x800')
font_style = ("Comic Sans MS", 10)
root.option_add("*Font", font_style)

def get_rgb(rgb):
    return "#%02x%02x%02x" % rgb 

style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background=get_rgb((118, 227, 131)), foreground="black")
style.map('Treeview', background=[('selected', get_rgb((73, 140,81)))])
def clear_root():
    for widget in root.winfo_children():
        widget.destroy()
    print(user_role)
    show_menu(role=user_role)
def show_employ():
    clear_root()
    employ_frame = LabelFrame(root, text='Сотрудники')
    employ_frame.pack(pady=10)

    image = Image.open('icon.png')
    photo = ImageTk.PhotoImage(image)

    icon_label = Label(employ_frame, image=photo)
    icon_label.pack(side="right", padx=5)

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

    employ_tree.bind("<<TreeviewSelect>>", lambda event: show_selected_item_employ(event, employ_tree, name_entry, password_entry, role_combobox, status_combobox))

    employ_data_frame = LabelFrame(root, text='Данные сотрудника')
    employ_data_frame.pack(padx=20)

    name_label = Label(employ_data_frame, text="Имя").grid(row=1, column=0, padx=10, pady=10)
    name_entry = Entry(employ_data_frame,)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = Label(employ_data_frame, text="Пароль").grid(row=1, column=4, padx=10, pady=10)
    password_entry = Entry(employ_data_frame)
    password_entry.grid(row=1, column=5, padx=10, pady=10)

    role_label = Label(employ_data_frame, text="Роль").grid(row=1, column=2, padx=10, pady=10)
    role_combobox = ttk.Combobox(employ_data_frame, values=['Повар', 'Официант'], state='readonly')
    role_combobox.grid(row=1, column=3, padx=10, pady=10)


    status_label = Label(employ_data_frame, text="Статус").grid(row=1, column=6, padx=10, pady=10)
    status_combobox = ttk.Combobox(employ_data_frame, values=['Активен','Уволен'], state='readonly')
    status_combobox.grid(row=1, column=7, padx=10, pady=10)

    employ_action_frame = LabelFrame(root, text='Команды')
    employ_action_frame.pack(fill='x', expand='yes', padx=20)

    add_employee_button = Button(employ_action_frame, background=get_rgb((73, 140,81)), text="Добавить", command=lambda: add_employ(name_entry,role_combobox,password_entry,status_combobox,employ_tree)).grid(row=0, column=0, padx=10, pady=10)
    update_employee_button = Button(employ_action_frame,background=get_rgb((73, 140,81)), text="Обновить", command= lambda: update_employ(name_entry, role_combobox, password_entry, status_combobox, employ_tree))
    update_employee_button.grid(row=0, column=1, padx=10, pady=10)

def show_shift():
    clear_root()
    
    shift_frame = LabelFrame(root, text='Смены')
    shift_frame.pack(pady=10)


    shift_scroll = Scrollbar(shift_frame)
    shift_scroll.pack(side='right', fill='y')
    shift_tree = ttk.Treeview(shift_frame, yscrollcommand=shift_scroll.set, selectmode='extended')
    shift_tree.pack()
    shift_scroll.config(command=shift_tree.yview)
    

    shift_tree['columns'] = ('ID', 'shiftType','employees')
    shift_tree.column('#0', width=0, anchor=W)
    shift_tree.column('ID', width=10, anchor=W)
    shift_tree.column('shiftType', width=100, anchor=CENTER)
    shift_tree.column('employees', width=140, anchor=CENTER)

    shift_tree.heading('#0', text='', anchor=W)
    shift_tree.heading('ID', text='ID', anchor=W)
    shift_tree.heading('shiftType', text='Тип смены', anchor=W)
    shift_tree.heading('employees', text='Сотрудники', anchor=CENTER)

    cursor.execute('''
    SELECT shift.id, shift.shift_type,users.username
    FROM shift
    INNER JOIN users ON shift.supervisor_id = users.id''')
    records = cursor.fetchall()
    for row in records:
        shift_tree.insert('', 'end', values=row)
        

    data_shift_frame = LabelFrame(root, text="Данные смены")
    data_shift_frame.pack(padx=10, pady=10, fill='both')

    def get_all_employees():
        global all_employees
        cursor.execute("SELECT username FROM users")
        all_employees = [row[0] for row in cursor.fetchall()]
        return all_employees

    employ_list = ttk.Combobox(data_shift_frame, state='readonly')
    employ_list.grid(row=0, column=3, padx=5, pady=5)

    all_employees = get_all_employees()
    employ_list['values'] = all_employees

    shift_label = Label(data_shift_frame, text='Тип смены')
    shift_label.grid(row=0, column=0, padx=5, pady=5)
    shift_type_entry = ttk.Combobox(data_shift_frame, values=['Утреняя','Вечерняя'], state='readonly')
    shift_type_entry.grid(row=0, column=1, padx=5, pady=5)
    employ_label = Label(data_shift_frame, text='Сотрудники')
    employ_label.grid(row=0, column=2, padx=5, pady=5)
    

    action_frame = LabelFrame(root, text="Действия")
    action_frame.pack(padx=10, pady=20, fill='both')

    add_button = Button(action_frame, background=get_rgb((73, 140,81)), text='Добавить', command=lambda: add_shift(shift_type_entry,employ_list,shift_tree))
    add_button.grid(row=1, column=0, padx=0, pady=0)

    shift_tree.bind('<<TreeviewSelect>>', lambda event: show_selected_item_shift(event, shift_tree, shift_type_entry, employ_list))

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
        order_tree.column('table', width=100, anchor=CENTER)
        order_tree.column('items', width=100, anchor=CENTER)
        order_tree.column('status', width=100, anchor=CENTER)
        order_tree.column('supervisor', width=100, anchor=CENTER)

        order_tree.heading('#0', text='', anchor=W)
        order_tree.heading('ID', text='ID', anchor=W)
        order_tree.heading('table', text='Номер столика', anchor=CENTER)
        order_tree.heading('count', text='Количество гостей', anchor=CENTER)
        order_tree.heading('items', text='Список заказа', anchor=CENTER)
        order_tree.heading('supervisor', text='Сотрудник', anchor=CENTER)
        order_tree.heading('status', text='Статус заказа', anchor=CENTER)

        order_scroll.config(command=order_tree.yview)


        cursor.execute('''
        SELECT orders.id, orders.table_number, orders. count, orders.items, orders.status, users.username, users.id
        FROM orders
        INNER JOIN users ON orders.supervisor_id = users.id
        ''')
        employ_list=[]
        employs_id = {}
        records = cursor.fetchall()
        for row in records:
            order_tree.insert('', 'end', values=row)
            employ_list.append(row[5])
            employs_id[row[5]]=row[6]

        order_data_frame = LabelFrame(root, text='Данные о заказе')
        order_data_frame.pack(padx=20, pady=10, fill='both')
        action_order_frame = LabelFrame(root, text='Команды')
        action_order_frame.pack(pady=10)
        
        if user_role=='Повар':
            table_entry = Entry(order_data_frame, state='readonly')
            user_entry = Entry(order_data_frame,state='readonly')
            Label(order_data_frame, text='Номер столика').grid(row=0, column=0, padx=5, pady=5)
            Label(order_data_frame, text='Количество гостей').grid(row=0, column=1, padx=5, pady=5)
            Label(order_data_frame, text='Список заказа').grid(row=0, column=2, padx=5, pady=5)
            Label(order_data_frame, text='Сотрудник').grid(row=0, column=3, padx=5, pady=5)
            Label(order_data_frame, text='Статус заказа').grid(row=0, column=4, padx=5, pady=5)
            count_entry = Entry(order_data_frame, state='readonly')
            count_entry.grid(row=1, column=1, padx=5, pady=5)
            item_entry = Entry(order_data_frame, state='readonly')
            item_entry.grid(row=1, column=2, padx=5, pady=5)
            table_entry.grid(row=1, column=0, padx=5, pady=5)
            status_order = ttk.Combobox(order_data_frame, values=('Готов','Готовится'), state='readonly')
            status_order.grid(row=1, column=4, padx=5, pady=5)
            user_entry.grid(row=1, column=3, padx=5, pady=5)
            order_tree.bind('<<TreeviewSelect>>',lambda event: show_selected_item_order(event,order_tree,table_entry,count_entry,item_entry,user_entry,status_order))

            Button(action_order_frame, background=get_rgb((73, 140,81)), text='Обновить', command=lambda: update_status(status_order, order_tree)).grid(row=4, column=0, padx=5, pady=5)


        elif user_role=='Официант':
            Label(order_data_frame, text='Номер столика').grid(row=1, column=0, padx=5, pady=5)
            table_entry = Entry(order_data_frame)
            table_entry.grid(row=2, column=0, padx=5, pady=5)
            Label(order_data_frame, text='Количество гостей').grid(row=1, column=2, padx=5, pady=5)
            count_entry = Entry(order_data_frame)
            count_entry.grid(row=2, column=2, padx=5, pady=5)
            Label(order_data_frame, text='Список заказа').grid(row=1, column=4, padx=5, pady=5)
            item_entry = Entry(order_data_frame)
            item_entry.grid(row=2, column=4, padx=5, pady=5)
            Label(order_data_frame, text='Сотрудник').grid(row=1, column=6, padx=5, pady=5)
            user_entry = ttk.Combobox(order_data_frame, values=employ_list)
            user_entry.grid(row=2, column=6, padx=5, pady=5)
            Label(order_data_frame, text='Статус заказа').grid(row=1, column=8, padx=5, pady=5)
            status_order = ttk.Combobox(order_data_frame, values=['Принят','Оплачен'], state='readonly')
            status_order.grid(row=2, column=8, padx=5, pady=5)
            order_tree.bind('<<TreeviewSelect>>',lambda event: show_selected_item_order(event,order_tree,table_entry,count_entry,item_entry,user_entry,status_order))
            update_order_button = Button(action_order_frame, background=get_rgb((73, 140,81)), text='Обновить', command=lambda: update_status(status_order, order_tree)).grid(row=4, column=1, padx=5, pady=5)
            add_order_button = Button(action_order_frame, background=get_rgb((73, 140, 81)), text='Добавить', command=lambda: add_order(table_entry, count_entry, item_entry, status_order, user_entry, order_tree,employs_id))
            add_order_button.grid(row=3, column=1, padx=5, pady=5)

        elif user_role=='Администратор':
            order_data_frame.grid_remove()
            action_order_frame.grid_remove()
    main_menu = Menu(root)
    inf_menu = Menu(main_menu, tearoff=0)
    if role == 'Администратор':
        inf_menu.add_command(label='Сотрудники', command=show_employ)
        inf_menu.add_command(label='Смены', command=show_shift)

    inf_menu.add_command(label="Заказы", command=show_order)
    inf_menu.add_separator()
    inf_menu.add_cascade(label='Выход', command=return_to_auth_page)
    main_menu.add_cascade(label='Меню', menu=inf_menu)
    root.config(menu=main_menu)

def return_to_auth_page():
    clear_root()
    show_login_window() 
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
            cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (login, password))
            user_role = cursor.fetchone()
            if user_role:
                user_role = user_role[0]
                messagebox.showinfo('Успешная авторизация', 'Добро пожаловать!')
                auth_frame.pack_forget()
                show_menu(user_role)
            else:
                messagebox.showerror('Ошибка', 'Неверный логин или пароль')

    login_button = Button(auth_frame, text="Войти",background=get_rgb((118, 227, 131)), command=auth)
    login_button.grid(row=2, columnspan=2)

show_login_window()


def show_selected_item_employ(event, employ_tree, name_entry, password_entry, role_combobox, status_combobox):
    selected_item = employ_tree.selection()  # Получаем выбранный элемент в TreeView
    if selected_item:  # Проверяем, что выбран хотя бы один элемент
        item_values = employ_tree.item(selected_item, 'values')
        name_entry.delete(0, END)
        name_entry.insert(0, item_values[1])
        password_entry.delete(0, END)
        password_entry.insert(0, item_values[2])
        role_combobox.set(item_values[3])
        status_combobox.set(item_values[4])

def show_selected_item_shift(event, shift_tree, shift_type_entry, employ_list):
    selected_item = shift_tree.selection()
    if selected_item:
        item_values = shift_tree.item(selected_item, 'values')
        print(item_values)
        shift_type_entry.set(item_values[1])
        employ_list.set( item_values[2])

def show_selected_item_order(event,order_tree,table_entry,count_entry,item_entry,user_entry,status_order):
    selected_item = order_tree.selection()
    if selected_item:
            item_values = order_tree.item(selected_item, 'values')
            table_entry.delete(0, END)
            table_entry.insert(0, item_values[1])
            count_entry.delete(0, END)
            count_entry.insert(0, item_values[2])
            item_entry.delete(0, END)
            item_entry.insert(0, item_values[3])
            user_entry.delete(0, END)
            status_order.delete(0, END)
            status_order.set(item_values[4])
            user_entry.insert(0, item_values[5])
def add_employ(name_entry,role_combobox,password_entry,status_combobox,employ_tree):
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
        employ_tree.insert('','end', values=(cursor.lastrowid, name,password,role,status))
        messagebox.showinfo('Сообщение','Данные удачно сохранены')
    except Exception as e:
        conn.rollback()
        messagebox.showinfo('Сообщение', 'Не удалось сохранить данные')
def add_shift(shift_type_entry, employ_list, shift_tree):
    shift_type = shift_type_entry.get()
    employ = employ_list.get()
    if not shift_type or not employ:
        messagebox.showerror('Ошибка', 'Заполните все поля')
        return

    try:
        cursor.execute("INSERT INTO shift (shift_type, supervisor_id) VALUES (?, ?)", (shift_type, employ))
        conn.commit()
        shift_tree.insert('', 'end', values=(cursor.lastrowid, shift_type, employ))
        messagebox.showinfo('Сообщение', 'Данные успешно сохранены')
    except Exception as e:
        conn.rollback()
        messagebox.showerror('Ошибка', f'Не удалось сохранить данные: {str(e)}')
def update_employ(name_entry, role_combobox, password_entry, status_combobox,employ_tree):
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
        item_id, old_name, _, old_role, old_status = employ_tree.item(selected_item, "values")
        confirmation = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите обновить данные для {old_name}?")
        
        if confirmation:
            cursor.execute("UPDATE users SET username=?, role=?, password=?, status=? WHERE id=?", (name, role, password, status, item_id))
            conn.commit()


            employ_tree.item(selected_item, text="", values=(item_id, name, password, role, status))
            messagebox.showinfo("Сообщение", "Данные обновлены!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Ошибка", f"Не удалось обновить данные: {str(e)}")
def add_order(table_entry, count_entry, item_entry, status_order, employ_list, order_tree,employs_id):
    table = table_entry.get()
    count = count_entry.get()
    item = item_entry.get()
    status = status_order.get()
    employ = employ_list.get()
    if not count or not item or not status or not employ:
        messagebox.showinfo("Ошибка", "Пожалуйста, заполните все поля")
        return
    try:
        cursor.execute("INSERT INTO orders (table_number, count, items, status, supervisor_id) VALUES (?, ?, ?, ?, ?)", (table, count, item, status, employs_id[employ]))
        conn.commit()
        order_tree.insert('', 'end', values=(cursor.lastrowid, table, count, item, status, employ))
        messagebox.showinfo('Сообщение', 'Данные успешно сохранены')
    except Exception as e:
        conn.rollback()
        messagebox.showinfo('Сообщение', 'Не удалось сохранить данные')
def update_status(status_order,order_tree):
    selected_item = order_tree.focus()

    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите заказ для обновления статуса")
        return

    status = status_order.get()

    if not status:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите статус для обновления")
        return

    try:
        old_values = order_tree.item(selected_item, "values")
        confirmation = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите обновить статус заказа {old_values[0]} с '{old_values[4]}' на '{status}'?")


        if confirmation:
            cursor.execute("UPDATE orders SET status=? WHERE id=?", (status, old_values[0]))
            conn.commit()
            order_tree.item(selected_item, values=(old_values[0], old_values[1], old_values[2], old_values[3], status,old_values[5]))
            messagebox.showinfo("Сообщение", "Статус заказа успешно обновлен!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Ошибка", f"Не удалось обновить статус заказа: {str(e)}")
root.mainloop()
conn.close()
