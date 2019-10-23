import pathlib
from urllib.request import urlopen, Request
from urllib.error import URLError

from . import config


class ServiceAdapter:
    def __init__(self, **config):
        self._host = config.get("host")
        self._headers = {"Content-Type": "application/json"}

    def create_entity(self, name, fields):
        req = Request(
            self._host + "/entity",
            data=fields,
            headers=self._headers,
            method="PUT",
        )
        response = urlopen(req)

    def add_data(self, name, data):
        req = Request(
            self._host + "/add",
            data=data,
            headers=self._headers,
            method="POST",
        )
        response = urlopen(req)

    def fetch_data(self, name, id):
        with urlopen(f'{self._host}/{name}/{id}') as resp:
            return resp.read()



def execute():
    msg = "Bem vindo ao Tutorial de Mocks!"
    try:
        response = urlopen(config.INCENDIOS_CSV_FILE_LINK)
    except URLError as exc:
        msg = f"Could not get CSV file: {exc}"
    else:
        csvfile = pathlib.Path("dados_incendios_cf.csv")
        csvfile.write_text(response.read().decode("utf-8"))
        adapter = ServiceAdapter(**config.SERVICE_CONFIG)
    return msg
