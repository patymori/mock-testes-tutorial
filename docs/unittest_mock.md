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


### Mock.return_value
 * Permite definir o retorno __fixo__ de:
   * uma chamada de função ou método
   * de uma instanciação de classe
   * de um atributo
   * de uma propriedade


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
 * O _target_ deve ser uma string com o caminho de import do módulo/objeto. Ex: 'package.module.ClassName'
 * Se _new_ não é informado, o objeto _target_ é substituído com um _MagicMock_

Então, vamos ao `test_app.py`

```python
[...]

class TestExecuteOK(TestCase):
    def setUp(self):
        with mock.patch('core.app.urlopen') as self.mock_urlopen:
            self.result = app.execute()
  [...]
    def test_gets_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)

[...]
```

Estamos usando primeiro o _patch_ em um context manager, o que garante que somente neste momento o _urlopen_ do _core.app_ será substituído.

Rode o teste e corrija os erros até que a falha ocorra:

```bash
======================================================================
FAIL: test_gets_csvfile_from_urllink_in_config (tests.test_app.TestExecuteOK)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "my_project/tests/test_app.py", line 16, in test_gets_csvfile_from_urllink_in_config
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
test_gets_csvfile_from_urllink_in_config (tests.test_app.TestExecuteOK) ... ok
test_returns_hello_app (tests.test_app.TestExecuteOK) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
```

Neste nosso exemplo, também poderíamos usar o _patch_ como decorador:

```python
[...]

class TestExecuteOK(TestCase):
    @mock.patch('core.app.urlopen')
    def setUp(self, mock_urlopen):
        self.mock_urlopen = mock_urlopen
        self.result = app.execute()
  [...]
    def test_gets_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)

[...]
```

Ou ainda criar um _patcher_, usando o `start()` e `stop()`:

```python
[...]

class TestExecuteOK(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_urlopen_patcher = mock.patch('core.app.urlopen')
        cls.mock_urlopen = cls.mock_urlopen_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_urlopen_patcher.stop()

    def setUp(self):
        self.result = app.execute()
  [...]
    def test_gets_csvfile_from_urllink_in_config(self):
        self.mock_urlopen.assert_called_once_with(config.INCENDIOS_CSV_FILE_LINK)

[...]
```

## Problema: salvar o arquivo CSV baixado

O `execute()` deverá salvar o arquivo CSV baixado em disco. Para isso, podemos:

 * Abrir um arquivo
 * Escrever o conteúdo recebido no arquivo

Vamos utilizar aqui `pathlib` para manipular o arquivo CSV. Nesta implementação, vamos usar especificamente `pathlib.Path`.

```python
[...]

class TestExecuteOK(TestCase):
    @classmethod
    def setUpClass(cls):
        [...]
        cls.mock_path_patcher = mock.patch.object(
            app.pathlib, 'Path', spec=app.pathlib.Path, name="MockPath"
        )
        cls.mock_path = cls.mock_path_patcher.start()

    @classmethod
    def tearDownClass(cls):
        [...]
        cls.mock_path_patcher.stop()

    def setUp(self):
        self.result = app.execute()

    [...]

    def test_creates_path_to_csvfile(self):
        self.mock_path.assert_called_with("dados_incendios_cf.csv")

    def test_writes_csvfile_content(self):
        self.mock_path.return_value.write_text.assert_called_with(self.mock_urlopen())

[...]
```


### _mock.patch.object(target, attribute, new=DEFAULT, **kwargs)_

Pode ser usado decorando uma método de teste, uma classe de teste ou em um context manager

O _target_ deve ser o caminho de import do módulo que contém o objeto a ser simulado. Atenção aqui que este caminho não é uma string!

O _attribute_ deve ser uma string com o nome do módulo/objeto a ser simulado

Se _new_ não é informado, o _attribute_ é substituído com um _MagicMock_


### _Mock spec e spec_set_

#### _spec_

O _spec_ é um argumento na definição de um dublê de teste. Pode ser uma lista de strins ou um objeto existente (uma classe ou instancia) que atua como a especificação para o dublê. Se um objeto é passado, então uma lista de strings é formada pela chamada do _dir()_ do objeto, excluindo os atributos e métodos mágicos não suportados. Acessando qualquer atributo ou método que não estiver na lista resultará na exceção _AttributeError_.

Um outro detalhe é que usando o _spec_ com um objeto, o atributo mágico *\_\_class\_\_* retorna a classe definida no _spec_. Isso permite que, por exemplo, a função _isinstance()_ funcione.


Rodando os testes, devem ocorrer os erros:

```bash
======================================================================
FAIL: test_creates_path_to_csvfile (tests.test_app.TestExecuteOK)
----------------------------------------------------------------------
Traceback (most recent call last):
 File "my_project/tests/test_app.py", line 37, in test_creates_path_to_csvfile
   self.mock_path.assert_called_with("dados_incendios_cf.csv")
 File "/home/username/.pyenv/versions/3.7.4/lib/python3.7/unittest/mock.py", line 825, in assert_called_with
   raise AssertionError('Expected call: %s\nNot called' % (expected,))
AssertionError: Expected call: open('dados_incendios_cf.csv')
Not called

======================================================================
FAIL: test_writes_csvfile_content (tests.test_app.TestExecuteOK)
----------------------------------------------------------------------
Traceback (most recent call last):
 File "my_project/tests/test_app.py", line 40, in test_writes_csvfile_content
   self.mock_path.return_value.write_text.assert_called_with(self.mock_urlopen())
 File "/home/username/.pyenv/versions/3.7.4/lib/python3.7/unittest/mock.py", line 825, in assert_called_with
   raise AssertionError('Expected call: %s\nNot called' % (expected,))
AssertionError: Expected call: write(<MagicMock name='urlopen()' id='140481532837584'>)
Not called

----------------------------------------------------------------------

```

E agora é implementar para o teste passar:

```python

[...]

def execute():

    [...]
    csvfile = pathlib.Path("dados_incendios_cf.csv")
    csvfile.write_text(response)
    return msg

 ```

Agora os testes devem passar.

```bash
test_creates_path_to_csvfile (tests.test_app.TestExecuteOK) ... ok
test_gets_csvfile_from_urllink_in_config (tests.test_app.TestExecuteOK) ... ok
test_returns_hello_app (tests.test_app.TestExecuteOK) ... ok
test_writes_csvfile_content (tests.test_app.TestExecuteOK) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.007s

OK
```


## Problema: arquivo CSV indisponível

O `execute()` deverá salvar o arquivo CSV somente se conseguir recebê-lo. Então, para que a aplicação informe corretamente que o CSV está indisponível, é necessário verificar a resposta HTTP. Vamos então:

 * Ao fazer a requisição HTTP do arquivo CSV do link, verificar se ocorre erro
 * Se ocorrer erro, exibir mensagem com detalhes do problema e não tentar gravar o arquivo

E como é possível simular um erro, uma exceção?


### Mock.side_effect
Permite definir um comportamento ao chamar um objeto, que pode ser:
 * o lançamento de uma exceção
 * retornos diferentes a cada chamada, através da definição de uma lista (ou tupla)
 * uma função a ser executada


Então vamos ao teste:

```python
[...]

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

[...]
```

Rodando os testes, o seguinte erro deve ser apresentado:

```bash
======================================================================
ERROR: test_url_does_not_exist_should_not_create_path (tests.test_app.TestExecuteErrors)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/username/.pyenv/versions/3.7.4/lib/python3.7/unittest/mock.py", line 1209, in patched
    return func(*args, **keywargs)
  File "my_project/tests/test_app.py", line 49, in test_url_does_not_exist_should_not_create_path
    self.result = app.execute()
  File "my_project/core/app.py", line 17, in execute
    response = urlopen(config.INCENDIOS_CSV_FILE_LINK)
  File "/home/username/.pyenv/versions/3.7.4/lib/python3.7/unittest/mock.py", line 965, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/home/username/.pyenv/versions/3.7.4/lib/python3.7/unittest/mock.py", line 1025, in _mock_call
    raise effect
urllib.error.URLError: <urlopen error [Errno -2] Name or service not known>

----------------------------------------------------------------------

```


Implementando para o teste passar...

```python

[...]

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

 ```

... e eles devem passar!

```bash
test_url_does_not_exist_should_not_create_path (tests.test_app.TestExecuteErrors) ... ok
test_creates_path_to_csvfile (tests.test_app.TestExecuteOK) ... ok
test_gets_csvfile_from_urllink_in_config (tests.test_app.TestExecuteOK) ... ok
test_returns_hello_app (tests.test_app.TestExecuteOK) ... ok
test_writes_csvfile_content (tests.test_app.TestExecuteOK) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.007s

OK
```



### Mock wraps

## configure_mock

## call_args, call_args_list

## PropertyMock

## Deletar atributos

## Seal
