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

tests/test_string.py
```
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

## Como rodar um script de teste

`python -m unittest -v tests/test_string.py`
