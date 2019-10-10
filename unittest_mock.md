# unittest.mock

 * Biblioteca *Built-in* de Test Doubles
 * Incorporada desde a versão 3.3
 * Oferece os recursos básicos para testes unitários
 * Baseado no Design Pattern *Arrange-Act-Assert*

## Classe Mock()
 * Permite a criação de Dublês de Teste de forma simples
 * Cria todos os atributos e métodos conforme são usados

Prompt do Python:
```
from unittest import mock
class ContaDaInternet:
    ...

conta = ContaDaInternet()
conta.obtem_status = mock.Mock(return_value="Paga")
conta.obtem_status()
```

 * return_value
 * spec e spec_set
 * side_effect
 * wraps

## Classe MagicMock()

## patch()
  * new_callable

## configure_mock

## call_args, call_args_list

## PropertyMock

## Deletar atributos

## Seal
