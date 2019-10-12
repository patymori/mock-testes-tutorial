import json
from unittest import TestCase, main, mock
from urllib.request import urlopen

from core import app


class TestExecute(TestCase):
    def setUp(self):
        self.result = app.execute()

    def test_returns_hello_app(self):
        self.assertEqual(self.result, "Bem vindo ao Tutorial de Mocks!")


if __name__ == '__main__':
    main()
