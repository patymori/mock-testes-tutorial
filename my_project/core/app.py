import pathlib
from urllib.request import urlopen

from . import config


def execute():
    msg = "Bem vindo ao Tutorial de Mocks!"
    response = urlopen(config.INCENDIOS_CSV_FILE_LINK)
    csvfile = pathlib.Path("dados_incendios_cf.csv")
    csvfile.write_text(response)
    return msg
