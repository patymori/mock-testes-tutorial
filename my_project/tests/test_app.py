import urllib
from unittest import TestCase, main, mock

from core import app, config


@mock.patch('core.app.urlopen', autospec=True)
@mock.patch('core.app.Request', autospec=True)
class TestServiceAdapter(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.headers = {
            "Content-Type": "application/json",
        }
        cls.service_config = {
            "host": "http://datastoreservice:8000",
        }
        cls.adapter = app.ServiceAdapter(**cls.service_config)

    def test_init(self, MockRequest, mock_urlopen):
        self.assertEqual(self.adapter._host, self.service_config["host"])
        self.assertEqual(self.adapter._headers, {"Content-Type": "application/json"})

    def test_create_entity(self, MockRequest, mock_urlopen):
        fields = {
            "field_1": {
                "type": "string",
                "mandatory": True,
            },
            "field_2": {
                "type": "integer",
                "mandatory": True,
            },
            "field_3": {
                "type": "date",
                "mandatory": False,
            },
            "field_4": {
                "type": "boolean",
                "mandatory": False,
            },
        }
        self.adapter.create_entity(name="test", fields=fields)
        MockRequest.assert_called_once_with(
            f'{self.service_config["host"]}/entity',
            data=fields,
            headers=self.headers,
            method="PUT",
        )
        mock_urlopen.assert_called_once_with(MockRequest.return_value)

    def test_add_data(self, MockRequest, mock_urlopen):
        data = {
            "field_1": "APA Costa das Algas",
            "field_2": "integer",
            "field_4": "boolean",
        }
        self.adapter.add_data(name="test", data=data)
        MockRequest.assert_called_once_with(
            f'{self.service_config["host"]}/add',
            data=data,
            headers=self.headers,
            method="POST",
        )
        mock_urlopen.assert_called_once_with(MockRequest.return_value)

    def test_fetch_data(self, MockRequest, mock_urlopen):
        data_dict = {
            "field_1": "APA Costa das Algas",
            "field_2": "integer",
            "field_4": "boolean",
        }
        data = str(data_dict).encode("utf-8")
        mock_handler = mock.Mock()
        mock_handler.read.return_value = data
        MockResponse = mock.MagicMock()
        MockResponse.__enter__.return_value = mock_handler
        mock_urlopen.return_value = MockResponse

        result = self.adapter.fetch_data(name="test", id="1234")

        self.assertIsNotNone(result)
        self.assertEqual(result, data)
        mock_urlopen.assert_called_once_with(f'{self.service_config["host"]}/test/1234')


class TestExecuteOK(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_urlopen_patcher = mock.patch('core.app.urlopen')
        cls.mock_urlopen = cls.mock_urlopen_patcher.start()

        cls.mock_path_patcher = mock.patch.object(
            app.pathlib, 'Path', autospec=True, name="MockPath"
        )
        cls.mock_path = cls.mock_path_patcher.start()

        cls.mock_service_adapter_patcher = mock.patch(
            'core.app.ServiceAdapter',
            autospec=True,
            name="MockServiceAdapter",
        )
        cls.mock_service_adapter = cls.mock_service_adapter_patcher.start()
        cls.service_config = {
            "host": "https://localhost:8888",
        }
        cls.mock_service_config_patcher = mock.patch.dict(
            'core.config.SERVICE_CONFIG', **cls.service_config
        )
        cls.mock_service_config = cls.mock_service_config_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_urlopen_patcher.stop()
        cls.mock_path_patcher.stop()
        cls.mock_service_adapter_patcher.stop()
        cls.mock_service_config_patcher.stop()

    def setUp(self):
        self.result = app.execute()

    def test_returns_hello_app(self):
        self.assertEqual(self.result, "Bem vindo ao Tutorial de Mocks!")

    def test_gets_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_with(config.INCENDIOS_CSV_FILE_LINK)

    def test_creates_path_to_csvfile(self):
        self.mock_path.assert_called_with("dados_incendios_cf.csv")

    def test_writes_csvfile_content(self):
        self.mock_path.return_value.write_text.assert_called_with(
            self.mock_urlopen.return_value.read.return_value.decode.return_value
        )

    def test_gets_service_adapter(self):
        self.mock_service_adapter.assert_called_with(**self.service_config)


class TestExecuteErrors(TestCase):
    @mock.patch('core.app.urlopen')
    @mock.patch('core.app.pathlib.Path')
    def test_url_does_not_exist_should_not_create_path(self, MockPath, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError(
          "[Errno -2] Name or service not known"
        )

        self.result = app.execute()

        self.assertEqual(
          self.result,
          "Could not get CSV file: <urlopen error [Errno -2] Name or service not known>"
        )
        MockPath.assert_not_called()


if __name__ == '__main__':
    main()
