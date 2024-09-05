from tkinter import *
import tkinter as tk
from tkinter import ttk


def configure_app(app):
    app.title('Análise e Desenvolvimento de Sistemas')
    app.geometry('1024x600')
    app.configure(background='#F8F8FF')
    app.resizable(True, True)
    app.maxsize(width=1024, height=600)


def create_frame(app):
    frame = LabelFrame(app, text=' Cadastro ', borderwidth=1,
                       relief='solid')
    frame.place(x=10, y=10, width=1000, height=200)
    return frame


def create_labels(frame):
    lb_1 = Label(frame, text='Contatos: ', fg='red',
                 font=('Arial', 14, 'italic', 'bold'))
    lb_1.place(x=15, y=10, width=70, height=20)
    lb_first_name = Label(frame, text='Digite um nome: ',
                          font=('Arial', 14))
    lb_first_name.place(x=20, y=35, width=120, height=20)
    lb_last_name = Label(frame, text='Digite um sobrenome: ',
                         font=('Arial', 14))
    lb_last_name.place(x=20, y=65, width=180, height=20)


def create_entry(frame):
    first_name = Entry(frame, font=('Arial', 14))
    first_name.place(x=200, y=35, width=400, height=20)
    last_name = Entry(frame, font=('Arial', 14))
    last_name.place(x=200, y=65, width=400, height=20)
    return first_name, last_name


def create_checkbutton(frame, gender_var):
    genders = ['Masculino', 'Feminino', 'Outros']
    y_pos = 95
    for gender in genders:
        Radiobutton(frame, text=gender, variable=gender_var, value=gender,
                    font=('Arial', 14)).place(x=200, y=y_pos)
        y_pos += 30


def create_button(app, capture, show_search_field, save_edit, delete_record, close_search, app_quit):
    style = ttk.Style()
    style.configure('Green.TButton', font=(
        'Arial', 14, 'bold'), background='#90EE90')
    style.configure('Blue.TButton', font=(
        'Arial', 14, 'bold'), background='#ADD8E6')
    style.configure('Red.TButton', font=(
        'Arial', 14, 'bold'), background='#FFB6C1')

    capture_btn = ttk.Button(app, text='Inserir dados',
                             style='Green.TButton', command=capture)
    capture_btn.place(x=20, y=220, width=155, height=40)
    search_btn = ttk.Button(
        app, text='Pesquisar dados', style='Blue.TButton', command=show_search_field)
    search_btn.place(x=185, y=220, width=155, height=40)
    update_btn = ttk.Button(
        app, text='Atualizar dados', style='Green.TButton', command=save_edit)
    update_btn.place(x=350, y=220, width=155, height=40)
    delete_btn = ttk.Button(app, text='Apagar registro',
                            style='Red.TButton', command=delete_record)
    delete_btn.place(x=515, y=220, width=155, height=40)
    exit_btn = ttk.Button(
        app, text='Sair', style='Red.TButton', command=app_quit)
    exit_btn.place(x=685, y=220, width=155, height=40)

    return capture_btn


def create_search_field(app, search_field_var, filter_data, close_search):
    lb_search = Label(
        app, text='Digite o nome a pesquisar: ', font=('Arial', 14), bg='white')
    lb_search.place(x=10, y=270, width=220, height=20)
    search_entry = Entry(app, font=('Arial', 14),
                         textvariable=search_field_var)
    search_entry.place(x=230, y=270, width=370, height=20)
    search_entry.bind('<KeyRelease>', filter_data)
    close_search_btn = ttk.Button(
        app, text='Fechar pesquisa', style='Blue.TButton', command=close_search)
    close_search_btn.place(x=610, y=265, width=155, height=30)


def create_treeview(app, on_item_double_click):
    columns = ('first_name', 'last_name', 'gender')
    tree = ttk.Treeview(app, columns=columns, show='headings')

    tree.heading('first_name', text='Nome')
    tree.heading('last_name', text='Sobrenome')
    tree.heading('gender', text='Gênero')

    tree.column('first_name', minwidth=0, width=250)
    tree.column('last_name', minwidth=0, width=250)
    tree.column('gender', minwidth=0, width=100)

    tree.place(x=10, y=300, width=1000, height=290)

    tree.bind("<Double-1>", on_item_double_click)

    return tree
