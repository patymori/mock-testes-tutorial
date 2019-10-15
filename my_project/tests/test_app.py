import json
from unittest import TestCase, main, mock

from core import app, config


class TestExecuteOK(TestCase):
    @mock.patch('core.app.urlopen')
    def setUp(self, mock_urlopen):
        self.mock_urlopen = mock_urlopen
        self.result = app.execute()

    def test_returns_hello_app(self):
        self.assertEqual(self.result, "Bem vindo ao Tutorial de Mocks!")

    def test_get_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)


if __name__ == '__main__':
    main()
