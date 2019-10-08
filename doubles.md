# Test Doubles (ou Mocks para os íntimos)

- Dummy: Objetos que podem circular quando necessário mas não tem nenhum tipo de implementação de teste e não deve ser usado pela aplicação
- Fake: Objetos que, normalmente, tem implementação simplificada de uma determinada interface é adequada para teste mas não para produção
- Stub: Objetos que oferecem implementações com respostas semiprontas que são adequadas para os testes
- Spies: Objetos que oferecem implementações que guardam valores que foram passados e que podem ser usados pelos testes
- Mocks: Objetos pré-programados para esperar chamadas específicas, número de vezes que uma chamada é feita e parâmetros e podem lançar exceções quando necessário
