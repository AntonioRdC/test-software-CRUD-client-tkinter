import unittest
import os
import json
from unittest.mock import patch, mock_open
from model import validate_field, save_data_to_file, load_data_from_file


class TestModel(unittest.TestCase):

    @patch('tkinter.messagebox.showwarning')
    def test_validate_field_empty(self, mock_showwarning):
        result = validate_field("", "Nome")

        mock_showwarning.assert_called_once_with('Aviso', 'Nome inválido.')

        self.assertFalse(result)

    @patch('tkinter.messagebox.showwarning')
    def test_validate_field_too_long(self, mock_showwarning):
        long_name = "A" * 51
        result = validate_field(long_name, "Nome")

        mock_showwarning.assert_called_once_with(
            'Aviso', 'Nome muito longo. Deve ter no máximo 50 caracteres.')

        self.assertFalse(result)

    @patch('tkinter.messagebox.showwarning')
    def test_validate_field_invalid_characters(self, mock_showwarning):
        result = validate_field("Nome123", "Nome")

        mock_showwarning.assert_called_once_with(
            'Aviso', 'Nome inválido. Não use números ou caracteres especiais.')

        self.assertFalse(result)

    def test_validate_field_valid(self):
        result = validate_field("João da Silva", "Nome")

        self.assertEqual(result, "João da Silva")

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_save_data_to_file(self, mock_file):
        person = {"nome": "João", "sobrenome": "Silva", "genero": "Masculino"}
        save_data_to_file(person)

        mock_file.assert_called_with("register.json", 'w')
        handle = mock_file()
        written_data = ''.join(call[0][0]
                               for call in handle.write.call_args_list)
        expected_data = json.dumps([person], indent=4)

        self.assertEqual(written_data, expected_data)

    @patch('os.path.exists', return_value=True)
    @patch('os.path.getsize', return_value=1)
    @patch('builtins.open', new_callable=mock_open, read_data='[{"nome": "João", "sobrenome": "Silva", "genero": "Masculino"}]')
    def test_load_data_from_file(self):
        result = load_data_from_file()

        self.assertEqual(result, [("João", "Silva", "Masculino")])

    @patch('os.path.exists', return_value=False)
    def test_load_data_from_file_empty(self):
        result = load_data_from_file()

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
