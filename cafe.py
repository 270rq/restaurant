import PySimpleGUI as sg
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Запросы к базе данных для получения данных
cursor.execute('SELECT * FROM users')
td_employees = cursor.fetchall()

cursor.execute('SELECT * FROM orders')
td_orders = cursor.fetchall()

cursor.execute('SELECT * FROM shift')
td_shift = cursor.fetchall()

cursor.close()
conn.close()

Headings_employees = ['Имя', 'Пароль', 'Роль', 'Статус']
Headings_orders = ['Номер столика', 'Количество гостей', 'Список заказа', 'Сотрудник', 'Статус']
Heading_shift = ['Тип смены', 'Сотрудник']

layout_login = [
    [sg.Text('Имя пользователя:'), sg.InputText(key='username')],
    [sg.Text('Пароль:'), sg.InputText(key='password', password_char='*')],
    [sg.Button('Войти')]
]

window_login = sg.Window('Авторизация', layout_login)
event, values = window_login.read()
window_login.close()

# аутентификация
if values['username'] == 'admin' and values['password'] == 'admin':
    layout_main = [
        [sg.TabGroup([
            [sg.Tab('Сотрудники', sg.Table(values=td_employees, headings=Headings_employees, key='employees'))],
            [sg.Tab('Заказы', sg.Table(values=td_orders, headings=Headings_orders, key='orders'))],
            [sg.Tab('Смены', sg.Table(values=td_shift, headings=Heading_shift, key='shift'))]
        ])]
    ]

    window_main = sg.Window('Кафе', layout_main)

    while True:
        event, values = window_main.read()
        if event == sg.WINDOW_CLOSED:
            break
else:
    sg.popup('Неверные учетные данные. Попробуйте снова.')

window_login.close()

layout_employees = [
    [sg.Text(Headings_employees[0]), sg.Input(s=15)],
    [sg.Text(Headings_employees[1]), sg.Input(s=15)],
    [sg.Text(Headings_employees[2]), sg.Combo(['Повар', 'Официант', 'Админ'], readonly=True)],
    [sg.Text(Headings_employees[3]), sg.Combo(['Активен', 'Уволен'], readonly=True)],
    [sg.Button('Добавить', key='add_employee')],
    [sg.Table(td_employees, Headings_employees, key='employees', enable_events=True, select_mode='browse')],
    [sg.Image('icon.png', subsample=3)]
]

layout_orders = [
    [sg.Text(Headings_orders[0]), sg.Input(s=15)],
    [sg.Text(Headings_orders[1]), sg.Input(s=15)],
    [sg.Text(Headings_orders[2]), sg.Input(s=15)],
    [sg.Text(Headings_orders[3]), sg.Combo(employees)],
    [sg.Text(Headings_orders[4]), sg.Combo(['Принят', 'Oплачен'], readonly=True)],
    [sg.Table(td_orders, Headings_orders, key='orders', enable_events=True, select_mode='browse')],
    [sg.Button('Добавить', key='add_order')],
    [sg.Image('icon.png', subsample=3)]
]

layout_shift = [
    [sg.Text(Heading_shift[0]), sg.Combo(['Утренняя', 'Вечерняя'], readonly=True)],
    [sg.Text(Heading_shift[1]), sg.Combo(employees, readonly=True)],
    [sg.Table(td_shift, Heading_shift, key='shift', enable_events=True, select_mode='browse')],
    [sg.Button('Добавить', key='add_shift')],
    [sg.Image('icon.png', subsample=3)]
]

layout_main = [
    [sg.TabGroup([
        [sg.Tab('Сотрудники', layout_employees)],
        [sg.Tab('Заказы', layout_orders)],
        [sg.Tab('Смены', layout_shift)]
    ])]
]

window_main = sg.Window('Кафе', layout_main)

while True:
    event, values = window_main.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'add_employee':
        td_employees.append(values.values())
        window_main['employees'].update(values=td_employees)
        for i in range(4):
            window_main[Headings_employees[i]].update(value='')

    elif event == 'add_order':
        td_orders.append(values.values())
        window_main['orders'].update(values=td_orders)

    elif event == 'add_shift':
        td_shift.append(values.values())
        window_main['shift'].update(values=td_shift)

    elif event == 'employees':
        selected_row = values['employees'][0]

cursor.close()
window_main.close()