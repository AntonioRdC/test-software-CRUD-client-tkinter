import unittest
from unittest.mock import MagicMock, patch
import controller
import model


class TestController(unittest.TestCase):

    def setUp(self):
        controller.app = MagicMock()
        controller.app.tree = MagicMock()

        controller.app.first_name_entry = MagicMock()
        controller.app.first_name_entry.get.return_value = "John"

        controller.app.last_name_entry = MagicMock()
        controller.app.last_name_entry.get.return_value = "John"

        controller.app.gender_var = MagicMock()
        controller.app.capture_btn = MagicMock()

    @patch('controller.model.validate_field', return_value='John')
    @patch('controller.model.save_data_to_file')
    def test_capture_valid(self, mock_save_data, mock_validate_field):
        controller.app.gender_var.get.return_value = 'Male'

        controller.capture(controller.app.first_name_entry, controller.app.last_name_entry,
                           controller.app.gender_var, controller.app.tree)
        mock_save_data.assert_called_once_with({
            'first_name': 'John',
            'last_name': 'John',
            'gender': 'Male'
        })
        self.assertEqual(controller.app.tree.insert.call_count, 1)

    @patch('controller.messagebox.showinfo')
    def test_save_edit_no_selection(self, mock_showinfo):
        controller.selected_person = None
        controller.save_edit(controller.app.first_name_entry, controller.app.last_name_entry,
                             controller.app.gender_var, controller.app.tree)
        mock_showinfo.assert_called_once_with(
            'Aviso', 'Nenhum registro selecionado para edição.')

    @patch('controller.json.dump')
    @patch('controller.os.path.exists', return_value=True)
    @patch('controller.os.path.getsize', return_value=100)
    @patch('controller.open', new_callable=unittest.mock.mock_open, read_data='[{"first_name": "John", "last_name": "John", "gender": "Male"}]')
    def test_save_edit_with_changes(self, mock_open, mock_getsize, mock_exists, mock_dump):
        controller.selected_person = ['John', 'John', 'Male']
        controller.app.gender_var.get.return_value = 'Female'

        controller.save_edit(controller.app.first_name_entry, controller.app.last_name_entry,
                             controller.app.gender_var, controller.app.tree)
        mock_dump.assert_called_once()
        self.assertEqual(controller.app.tree.insert.call_count, 1)

    @patch('controller.model.load_data_from_file', return_value=[('John', 'John', 'Male')])
    def test_close_search(self, mock_load_data):
        controller.app.tree.get_children.return_value = ['item1']
        controller.close_search(controller.app)
        controller.app.tree.delete.assert_called_once_with('item1')

    @patch('controller.messagebox.showwarning')
    def test_delete_record_no_selection(self, mock_showwarning):
        controller.app.tree.selection.return_value = []
        controller.delete_record(
            controller.app.tree, controller.app.capture_btn)
        mock_showwarning.assert_called_once_with(
            'Aviso', 'Selecione um registro para excluir!')

    @patch('controller.model.load_data_from_file', return_value=[('John', 'John', 'Male')])
    def test_filter_data(self, mock_load_data):
        mock_search_field_var = MagicMock()
        mock_search_field_var.get.return_value = 'John'

        controller.filter_data(
            MagicMock(), controller.app.tree, mock_search_field_var)
        controller.app.tree.insert.assert_called_once_with(
            '', 'end', values=('John', 'John', 'Male'))


if __name__ == '__main__':
    unittest.main()
