import io
import json
from unittest import TestCase, main, mock

from core import app, config


class TestExecuteOK(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_urlopen_patcher = mock.patch('core.app.urlopen')
        cls.mock_urlopen = cls.mock_urlopen_patcher.start()

        cls.mock_path_patcher = mock.patch.object(
            app.pathlib, 'Path', spec=app.pathlib.Path, name="MockPath"
        )
        cls.mock_path = cls.mock_path_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_urlopen_patcher.stop()
        cls.mock_path_patcher.stop()

    def setUp(self):
        self.result = app.execute()

    def test_returns_hello_app(self):
        self.assertEqual(self.result, "Bem vindo ao Tutorial de Mocks!")

    def test_gets_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_with(config.INCENDIOS_CSV_FILE_LINK)

    def test_creates_path_to_csvfile(self):
        self.mock_path.assert_called_with("dados_incendios_cf.csv")

    def test_writes_csvfile_content(self):
        self.mock_path.return_value.write_text.assert_called_with(self.mock_urlopen())


if __name__ == '__main__':
    main()
