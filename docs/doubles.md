# Test Doubles (ou Mocks para os íntimos)

 * Test Double não é Mock mas Mock é um Test Double
 * Dublês de Testes substituem objetos reais
  * Outro componente
  * Serviço
  * Banco de Dados

## Tipos de Dublês de Teste

### Dummy

Objetos que podem circular quando necessário mas não tem nenhum tipo de implementação de teste e não será usado pela aplicação.

### Fake

Objetos que, normalmente, tem implementação simplificada de uma determinada interface, que é adequada para teste mas não para produção.

Exemplos de aplicação: arquivo com conteúdo para o teste, data e hora de criação de um registro.

### Stub

Objetos que oferecem implementações com respostas semiprontas que são adequadas para os testes.

Exemplos de aplicação: status de uma transação.

### Spies

Objetos que oferecem implementações que guardam valores que foram passados e que podem ser usados pelos testes.

Exemplos de aplicação: atualização ou configuração de um valor que precisa ser verificado.

### Mocks

Objetos pré-programados para esperar chamadas específicas, número de vezes que uma chamada é feita e parâmetros e podem lançar exceções quando necessário.

Exemplos de aplicação: verificar se todos os dados de uma lista foram enviados para o banco de dados, falha na conexão com um serviço.
