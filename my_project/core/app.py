from urllib.request import urlopen

from . import config


def execute():
    msg = "Bem vindo ao Tutorial de Mocks!"
    urlopen(config.INCENDIOS_CSV_FILE_LINK)
    return msg
