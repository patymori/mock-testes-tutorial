# _unittest.mock_

 * Biblioteca *Built-in* de Test Doubles
 * Incorporada desde a versão 3.3
 * Oferece os recursos básicos para testes unitários
 * Baseado no padrão *Arrange-Act-Assert*

## Classe _Mock()_
 * Permite a criação de Dublês de Teste de forma simples
 * Cria todos os atributos e métodos conforme são usados


#### Exemplo de uso do _Mock_
```python
import json
from unittest import mock
from urllib.request import urlopen

class ContaDaInternet:
    def obtem_status():
        token = "ad18ce48280b0ab4cd19e719bec348b82e19ee56f05af78c9aef6d7f5bc444fd"
        response = urlopen(
            f"https://provedordeinternet.com.br/conta/{token}/?status")
        if response.status == 200:
            resp_json = json.loads(response.read())
            return resp_json.get("status")


conta = ContaDaInternet()
conta.obtem_status = mock.Mock(return_value="Paga")
conta.obtem_status()
```

## Classe _MagicMock()_
 * Subclasse de _Mock_, com o mesmo construtor
 * Todos os _magic methods_ são pré-criados e prontos para uso. Consulte a documentação para saber os valores de retorno padrão de cada método mágico.


## Problema: baixar o arquivo CSV no link

O `execute()` terá que acessar o link do site para gravar o arquivo CSV. Como o link pode mudar, vamos usar uma variável em um arquivo de configuração. Assim, é só alterar a configuração. Podemos pensar nos seguintes passos para realizar a tarefa:

 * Pegar link em config.py
 * HTTP GET no link
 * Ex: `urlopen(config.INCENDIOS_CSV_FILE_LINK)`

E como vou saber se o urlopen foi executado corretamente, passando a URL certa?


### _mock.patch(target, new=DEFAULT, **kwargs)_

 * Pode ser usado decorando uma método de teste, uma classe de teste ou em um context manager
 * O _target_ deve ser uma string com o "caminho do objeto". Ex: 'package.module.ClassName'
 * Se _new_ não é informado, o objeto _target_ é substituído com um _MagicMock_

Então, vamos ao `test_app.py`

```python
[...]

class TestExecute(TestCase):
    def setUp(self):
        with mock.patch('core.app.urlopen') as self.mock_urlopen:
            self.result = app.execute()
  [...]
    def test_get_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)


if __name__ == '__main__':
    main()
```

Estamos usando primeiro o _patch_ em um context manager, o que garante que somente neste momento o _urlopen_ do _core.app_ será substituído.

Rode o teste e corrija os erros até que a falha ocorra:

```bash
======================================================================
FAIL: test_get_csvfile_from_urllink_in_config (tests.test_app.TestExecuteOK)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "my_project/tests/test_app.py", line 16, in test_get_csvfile_from_urllink_in_config
    self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)
  File "/home/username/.pyenv/versions/3.7.4/lib/python3.7/unittest/mock.py", line 844, in assert_called_once_with
    raise AssertionError(msg)
AssertionError: Expected 'urlopen' to be called once. Called 0 times.

----------------------------------------------------------------------

```

Agora é hora de implementar o objeto do teste:

```python

from urllib.request import urlopen

from . import config


def execute():
    msg = "Bem vindo ao Tutorial de Mocks!"
    urlopen(config.INCENDIOS_CSV_FILE_LINK)
    return msg

```

Rodando os testes novamente, não deve haver mais falhas.

```bash
test_get_csvfile_from_urllink_in_config (tests.test_app.TestExecuteOK) ... ok
test_returns_hello_app (tests.test_app.TestExecuteOK) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
```

Neste nosso exemplo, também poderíamos usar o _patch_ como decorador:

```python
[...]

class TestExecute(TestCase):
    @mock.patch('core.app.urlopen')
    def setUp(self, mock_urlopen):
        self.mock_urlopen = mock_urlopen
        self.result = app.execute()
  [...]
    def test_get_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)


if __name__ == '__main__':
    main()
```


### Mock.return_value
 * Permite definir o retorno __fixo__ de:
   * uma chamada de função ou método
   * de uma instanciação de classe
   * de um atributo
   * de uma propriedade


###


### mock.patch(target, new=DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None)


### Mock spec e spec_set
### Mock.side_effect
### Mock wraps

## configure_mock

## call_args, call_args_list

## PropertyMock

## Deletar atributos

## Seal
