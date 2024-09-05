import unittest
from tkinter import Tk, StringVar, Entry, Radiobutton
from unittest.mock import MagicMock
from view import configure_app, create_frame, create_labels, create_entry, create_checkbutton, create_button, create_search_field, create_treeview


class TestView(unittest.TestCase):

    def setUp(self):
        self.app = Tk()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test_configure_app(self):
        configure_app(self.app)

    def test_create_frame(self):
        frame = create_frame(self.app)
        self.assertEqual(frame['text'], ' Cadastro ')
        self.assertEqual(frame['borderwidth'], 1)
        self.assertEqual(frame['relief'], 'solid')

    def test_create_labels(self):
        frame = create_frame(self.app)
        create_labels(frame)
        labels = frame.winfo_children()
        self.assertEqual(labels[0]['text'], 'Contatos: ')
        self.assertEqual(labels[1]['text'], 'Digite um nome: ')
        self.assertEqual(labels[2]['text'], 'Digite um sobrenome: ')

    def test_create_entry(self):
        frame = create_frame(self.app)
        first_name, last_name = create_entry(frame)
        self.assertEqual(first_name.winfo_class(), 'Entry')
        self.assertEqual(last_name.winfo_class(), 'Entry')

    def test_create_checkbutton(self):
        frame = create_frame(self.app)
        gender_var = StringVar()
        create_checkbutton(frame, gender_var)
        radios = frame.winfo_children()
        radio_buttons_text = [radio['text']
                              for radio in radios if isinstance(radio, Radiobutton)]
        self.assertIn('Masculino', radio_buttons_text)
        self.assertIn('Feminino', radio_buttons_text)
        self.assertIn('Outros', radio_buttons_text)

    def test_create_button(self):
        capture = MagicMock()
        show_search_field = MagicMock()
        save_edit = MagicMock()
        delete_record = MagicMock()
        close_search = MagicMock()
        app_quit = MagicMock()

        capture_btn = create_button(
            self.app, capture, show_search_field, save_edit, delete_record, close_search, app_quit)

        self.assertEqual(capture_btn['text'], 'Inserir dados')

    def test_create_search_field(self):
        search_field_var = StringVar()
        filter_data = MagicMock()
        close_search = MagicMock()
        create_search_field(self.app, search_field_var,
                            filter_data, close_search)
        children = self.app.winfo_children()
        entry = [child for child in children if isinstance(child, Entry)][0]
        self.assertEqual(entry.winfo_class(), 'Entry')

    def test_create_treeview(self):
        on_item_double_click = MagicMock()
        tree = create_treeview(self.app, on_item_double_click)
        self.assertEqual(
            tree['columns'], ('first_name', 'last_name', 'gender'))
        self.assertEqual(tree.heading('first_name')['text'], 'Nome')


if __name__ == '__main__':
    unittest.main()
