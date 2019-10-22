import pathlib
from urllib.request import urlopen
from urllib.error import URLError

from . import config


def execute():
    msg = "Bem vindo ao Tutorial de Mocks!"
    try:
        response = urlopen(config.INCENDIOS_CSV_FILE_LINK)
    except URLError as exc:
        msg = f"Could not get CSV file: {exc}"
    else:
        csvfile = pathlib.Path("dados_incendios_cf.csv")
        csvfile.write_text(response)
    return msg
