import os
import json
import regex as re
from tkinter import messagebox


def validate_field(field, field_type):

    if not field:

        messagebox.showwarning('Aviso', f'{field_type} inválido.')
        return False
    if len(field) > 50:
        messagebox.showwarning(
            'Aviso', f'{field_type} muito longo. Deve ter no máximo 50 caracteres.')
        return False

    pattern = r'^[\p{L}\s]{1,50}$'
    if not re.match(pattern, field):
        messagebox.showwarning(
            'Aviso', f'{field_type} inválido. Não use números ou caracteres especiais.')
        return False

    prepositions = ['da', 'de', 'do', 'das', 'dos']
    field = ' '.join([part.capitalize(
    ) if part not in prepositions else part for part in re.sub(r'\s+', ' ', field).split()])
    return field


def save_data_to_file(person):
    json_file = "register.json"
    data = []
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, 'r') as file:
            data = json.load(file)

    data.append(person)
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


def load_data_from_file():
    json_file = "register.json"
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, 'r') as file:
            return [(line['first_name'], line['last_name'], line['gender']) for line in json.load(file)]
    return []
