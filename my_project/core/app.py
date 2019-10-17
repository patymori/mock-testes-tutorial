from urllib.request import urlopen

from . import config


def execute():
    msg = "Bem vindo ao Tutorial de Mocks!"
    response = urlopen(config.INCENDIOS_CSV_FILE_LINK)
    with open("dados_incendios_cf.csv", "w") as csvfile:
        csvfile.write(response)
    return msg
