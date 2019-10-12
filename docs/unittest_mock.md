# unittest.mock

 * Biblioteca *Built-in* de Test Doubles
 * Incorporada desde a versão 3.3
 * Oferece os recursos básicos para testes unitários
 * Baseado no Design Pattern *Arrange-Act-Assert*

## Classe Mock()
 * Permite a criação de Dublês de Teste de forma simples
 * Cria todos os atributos e métodos conforme são usados

#### Exemplo de uso do Mock
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


#### Problema: 


###



### Mock spec e spec_set
### Mock.side_effect
### Mock wraps

## Classe MagicMock()

## patch()
  * new_callable

## configure_mock

## call_args, call_args_list

## PropertyMock

## Deletar atributos

## Seal
