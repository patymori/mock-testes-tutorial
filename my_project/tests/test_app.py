import io
import json
from unittest import TestCase, main, mock

from core import app, config


class TestExecuteOK(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_urlopen_patcher = mock.patch('core.app.urlopen')
        cls.mock_urlopen = cls.mock_urlopen_patcher.start()

        cls.mock_file = mock.Mock(name="MockCsvfile", spec_set=io.StringIO)
        file_handler = mock.MagicMock()
        file_handler.__enter__.return_value = cls.mock_file
        file_handler.__exit__.return_value = False
        cls.mock_open_patcher = mock.patch('builtins.open', spec=open)
        cls.mock_open = cls.mock_open_patcher.start()
        cls.mock_open.return_value = file_handler

    @classmethod
    def tearDownClass(cls):
        cls.mock_urlopen_patcher.stop()
        cls.mock_open_patcher.stop()

    def setUp(self):
        self.result = app.execute()

    def test_returns_hello_app(self):
        self.assertEqual(self.result, "Bem vindo ao Tutorial de Mocks!")

    def test_get_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)

    def test_open_cvsfile_in_write_mode(self):
        self.mock_open.assert_called_with("dados_incendios_cf.csv", "w")

    def test_write_csvfile_content(self):
        self.mock_file.write.assert_called_with(self.mock_urlopen())


if __name__ == '__main__':
    main()
