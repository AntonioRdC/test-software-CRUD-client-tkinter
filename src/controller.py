from tkinter import Tk, StringVar, messagebox, END, NORMAL
import os
import view
import model
import json

selected_person = None


def start_app():
    global app
    app = Tk()
    app.message_var = StringVar()
    app.gender_var = StringVar()
    app.search_field_var = StringVar()
    view.configure_app(app)
    frame = view.create_frame(app)
    view.create_labels(frame)
    app.first_name_entry, app.last_name_entry = view.create_entry(frame)

    view.create_checkbutton(frame, app.gender_var)

    app.capture_btn = view.create_button(app, lambda: capture(app.first_name_entry, app.last_name_entry, app.gender_var, app.tree),
                                         lambda: show_search_field(
                                             app, app.search_field_var),
                                         lambda: save_edit(
                                             app.first_name_entry, app.last_name_entry, app.gender_var, app.tree),
                                         lambda: delete_record(
                                             app.tree, app.capture_btn),
                                         lambda: close_search(app), app.quit)

    app.tree = view.create_treeview(
        app, lambda event: on_item_double_click(event))

    for person in model.load_data_from_file():
        app.tree.insert('', 'end', values=person)

    app.mainloop()


def on_item_double_click(event):
    global selected_person
    selection = app.tree.selection()
    if selection:
        item = app.tree.item(selection)
        selected_person = item['values']
        first_name, last_name, gender = item['values']

        app.first_name_entry.delete(0, END)
        app.first_name_entry.insert(0, first_name)
        app.last_name_entry.delete(0, END)
        app.last_name_entry.insert(0, last_name)
        app.gender_var.set(gender)


def capture(first_name, last_name, gender_var, tree):
    input_first_name = model.validate_field(first_name.get(), 'Nome')
    input_last_name = model.validate_field(last_name.get(), 'Sobrenome')
    selected_gender = app.gender_var.get()
    if selected_gender in [None, '', 'None']:
        messagebox.showwarning('Aviso', 'Selecione um gênero.')
        return

    if not input_first_name or not input_last_name:
        return

    person = {
        'first_name': input_first_name,
        'last_name': input_last_name,
        'gender': selected_gender
    }

    model.save_data_to_file(person)
    tree.insert('', 'end', values=(
        person['first_name'], person['last_name'], person['gender']))

    first_name.delete(0, 'end')
    last_name.delete(0, 'end')
    app.gender_var.set(None)


def show_search_field(app, search_field_var):
    app.message_var.set('')
    app.gender_var.set(None)
    app.search_field_var = search_field_var
    view.create_search_field(app, search_field_var,
                             lambda event: filter_data(event, app.tree, search_field_var), lambda: close_search(app))


def save_edit(first_name, last_name, gender_var, tree):
    global selected_person
    if selected_person is None:
        messagebox.showinfo(
            'Aviso', 'Nenhum registro selecionado para edição.')
        return

    input_first_name = model.validate_field(first_name.get(), 'Nome')
    input_last_name = model.validate_field(last_name.get(), 'Sobrenome')
    selected_gender = app.gender_var.get()

    if not input_first_name or not input_last_name or not selected_gender:
        return

    new_person = {
        'first_name': input_first_name,
        'last_name': input_last_name,
        'gender': selected_gender
    }

    if new_person == selected_person:
        messagebox.showinfo('Aviso', 'Nenhuma alteração detectada...')
        return

    data = []
    json_file = "register.json"
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, 'r') as file:
            data = json.load(file)

    for i, person in enumerate(data):
        if person['first_name'] == selected_person[0] and person['last_name'] == selected_person[1] and person['gender'] == selected_person[2]:
            data[i] = new_person
            break

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    for i in tree.get_children():
        tree.delete(i)
    for person in data:
        tree.insert('', 'end', values=(
            person['first_name'], person['last_name'], person['gender']))

    first_name.delete(0, 'end')
    last_name.delete(0, 'end')
    app.gender_var.set(None)
    selected_person = None
    app.capture_btn['state'] = NORMAL
    app.message_var.set("")


def delete_record(tree, capture_btn):
    global selected_person
    try:
        tree_selection = tree.selection()[0]
        selected_person = tree.item(tree_selection, 'values')
        confirm = messagebox.askyesno(
            "Confirmar Exclusão", "Tem certeza que deseja excluir este registro?")
        if confirm:
            data = []
            json_file = "register.json"
            if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
                with open(json_file, 'r') as file:
                    data = json.load(file)

            data = [person for person in data if not (
                person['first_name'] == selected_person[0] and person['last_name'] == selected_person[1] and person['gender'] == selected_person[2])]

            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)

            tree.delete(tree_selection)
    except IndexError:
        messagebox.showwarning('Aviso', 'Selecione um registro para excluir!')
    finally:
        capture_btn['state'] = 'normal'
        app.message_var.set("")
        app.gender_var.set(None)


def close_search(app):
    for i in app.tree.get_children():
        app.tree.delete(i)

    for person in model.load_data_from_file():
        app.tree.insert('', 'end', values=person)


def filter_data(event, tree, search_field_var):
    for i in tree.get_children():
        tree.delete(i)
    search_term = search_field_var.get()
    filtered_data = [person for person in model.load_data_from_file(
    ) if search_term.lower() in person[0].lower()]
    for person in filtered_data:
        tree.insert('', 'end', values=person)


if __name__ == '__main__':
    start_app()
