# Unittest: testes automatizados usando Just Python

 * Módulo *Built-in* do Python para testes unitários
 * Inspirado pelo JUnit, framework Java de testes unitários

## unittest.TestCase

 * Cenário único, com determinada configuração para o teste.
 * Criação de subclasses de `unittest.TestCase` ou `unittest.FunctionTestCase`

## unittest.TestSuite

 * Coleção de TestCases e outros TestSuites
 * Organizar testes que devem ser executados juntos

## Mão na massa 1: Como montar um caso de teste

Vamos montar um caso de teste de algo já implementado, para já irmos criando memória muscular. Também para vermos que é possível criar testes para o que já está desenvolvido, certo? ;-)

Nosso primeiro objeto de teste será o `str`!

_tests/test_string.py_
```python
import unittest


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('python'.upper(), 'PYTHON')

    def test_isupper(self):
        self.assertTrue('PYTHON'.isupper())
        self.assertFalse('Python'.isupper())

    def test_split(self):
        s = 'Python Brasil [15]'
        self.assertEqual(s.split(), ['Python', 'Brasil', '[15]'])
        with self.assertRaises(TypeError):
            s.split(3)


if __name__ == '__main__':
    unittest.main()
```

E para rodá-lo, basta executar o seguinte comando:

```bash
python -m unittest -v tests/test_string.py
```


## Mão na massa 2: Iniciando nosso projeto com testes (e TDD!)

Agora vamos criar um projeto do zero, usando TDD para nos guiar. Vamos utilizar este projeto para o restante do tutorial, tentando explorar casos de uso reais (ou mais próximos deles).

Nossa aplicação vai baixar um arquivo sobre os incêndios em Unidades de Conservação Federais entre 2012 e 2018 e vai armazenar os dados em um banco de dados, que será disponibilizado para análise.

O arquivo está em formato CSV e se encontra no link do Instituto Chico Mentes: http://www.icmbio.gov.br/acessoainformacao/images/stories/PDA/Planilhas/Planilhas_CSV/DIMIF-queima.csv, com os seguintes dados:
- Código CNUC
- Nome da UC
- Categoria da UC: sigla federal
- Categoria da UC: nomenclatura nacional
- Grupo de Proteção
- Ano de criação
- Coordenação Regional do ICMBio
- Área estimada da UC (ha)
- Bioma referencial
- Área queimada em 2018
- Área queimada em 2017
- Área queimada em 2016
- Área queimada em 2015
- Área queimada em 2014
- Área queimada em 2013
- Área queimada em 2012

O armazenamento dos dados será feito através de um serviço externo, que tem uma REST API.

Vamos começar montando a estrutura básica de um projeto:

```bash
my_project
├── tests
│   ├── __init__.py
│   └── test_app.py
├── README.md
└── setup.py
```

Agora, defina o conteúdo do `setup.py`:

_setup.py_
```python
import setuptools
import pathlib

readme_path = pathlib.Path("README.md")
with readme_path.open() as f:
    README = f.read()

setuptools.setup(
    name="my_project",
    version="0.1",
    author="Paty Morimoto",
    author_email="excermori@yahoo.com.br",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3.0",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    python_requires=">=3.7",
    test_suite="tests",
    classifiers=[
        "Development Status :: 2 - Beta",
        "Environment :: Other Environment",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    entry_points="""\
        [console_scripts]
            my_app=core.app:execute
    """,
)
```

... e a nossa classe de teste:

_tests/test_app.py_
```python
from unittest import TestCase, main

from core import app


class TestExecute(TestCase):
    def setUp(self):
        self.result = app.execute()

    def test_returns_hello_app(self):
        self.assertEqual(self.result, "Bem vindo ao Tutorial de Mocks!")


if __name__ == '__main__':
    main()
```

Pronto! A gente já consegue rodar o nosso primeiro teste com TDD!

```bash
python setup.py test
```

E ver nosso primeiro erro:

```bash
[...]

test_returns_hello_app (tests.test_app.TestExecute) ... ERROR

======================================================================
ERROR: test_returns_hello_app (tests.test_app.TestExecute)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../my_project/tests/test_app.py", line 10, in setUp
    self.result = app.execute()
AttributeError: module 'core.app' has no attribute 'execute'

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
Test failed: <unittest.runner.TextTestResult run=1 errors=1 failures=0>
error: Test failed: <unittest.runner.TextTestResult run=1 errors=1 failures=0>
```

Vamos corrigindo _ERROR_, até começarem a ocorrer _FAIL_ e, finalmente, ter nossa implementação com o teste rodando.
A mensagem de erro acima indica que está faltando a função `execute` no modulo: `core.app`, para resolver isso precisamos escrever este código:

_core/app.py_
```python
def execute():
    return "Bem vindo ao Tutorial de Mocks!"
```

Ao final desta primeira etapa, teremos esta árvore de projeto:

```bash
my_project
├── core
│   ├── app.py
│   └── __init__.py
├── tests
│   ├── __init__.py
│   └── test_app.py
├── README.md
└── setup.py
```

Rodando novamente os testes:

```bash
python setup.py test
```
a saida deve ser assim:
```bash
running test
running egg_info
writing my_project.egg-info/PKG-INFO
writing dependency_links to my_project.egg-info/dependency_links.txt
writing entry points to my_project.egg-info/entry_points.txt
writing top-level names to my_project.egg-info/top_level.txt
reading manifest file 'my_project.egg-info/SOURCES.txt'
writing manifest file 'my_project.egg-info/SOURCES.txt'
running build_ext
test_returns_hello_app (tests.test_app.TestExecute) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
