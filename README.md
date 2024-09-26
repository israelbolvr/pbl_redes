# Sistema de Compra de Passagens Aéreas - Projeto PBL Redes

Este relatório documenta o **Sistema de Compra de Passagens Aéreas**, desenvolvido como parte da disciplina de Redes e Sistemas Distribuídos. O sistema implementa uma arquitetura cliente-servidor para uma companhia aérea low-cost, permitindo a consulta e compra de passagens de voos disponíveis.

## Equipe de Desenvolvimento

- **Felipe Freitas Alves**
- **Israel Vítor Barreto de Oliveira**

## Arquitetura da Solução

A arquitetura do sistema foi desenvolvida utilizando o modelo cliente-servidor, com comunicação baseada em sockets TCP e troca de mensagens prefixadas. Os componentes e seus papéis na arquitetura são:

- **Servidor** (`server.py`): Responsável por gerenciar os recursos do sistema, como voos, vagas e passageiros. Ele lida com múltiplas conexões de clientes simultaneamente, utilizando threads para cada conexão. O servidor mantém o estado das sessões dos passageiros durante a interação.

- **Clientes** (`client.py` e `test_client.py`): Aplicações que permitem aos passageiros interagir com o sistema, realizando operações como login, consulta de voos e reserva de assentos. O `client.py` permite interação manual, enquanto o `test_client.py` simula múltiplos clientes para testes de conexões simultâneas e perda de conexão. Cada cliente é executado em um contêiner Docker separado para simular usuários distintos.

- **Modelos** (`Models/`): Contém as classes que representam as entidades do sistema:
  - `Voo.py`: Representa um voo, contendo informações como ID, data, local de saída e destino.
  - `Vaga.py`: Representa uma vaga (assento) em um voo, incluindo status e controle de concorrência.
  - `Passageiro.py`: Representa um passageiro, com dados pessoais e autenticação.
  - `Passagem.py`: Representa uma passagem emitida para um passageiro específico.

## Paradigma de Comunicação

O paradigma de serviço utilizado é o **stateful**. O servidor mantém o estado da sessão de cada passageiro após o login, permitindo que ele realize múltiplas operações sem a necessidade de reautenticação. Essa escolha foi motivada pela necessidade de manter informações de contexto durante as interações, proporcionando uma experiência mais consistente e personalizada para o usuário.

### Protocolo de Comunicação

O protocolo de comunicação entre o cliente e o servidor utiliza sockets TCP com mensagens prefixadas pelo tamanho, garantindo a entrega completa dos dados. As mensagens são serializadas usando o módulo `pickle` do Python, com um prefixo de 4 bytes indicando o tamanho da mensagem.

#### Estrutura das Mensagens

As mensagens trocadas entre o cliente e o servidor seguem uma estrutura padronizada de dicionários Python serializados, que incluem um campo de **ação** e dados específicos para cada operação.

##### 1. **Login de Passageiro**

O cliente envia os dados de login ou cadastro do passageiro.

**Mensagem do Cliente:**

```python
{
    "action": "login",
    "cpf": "12345678900",
    "senha": "senhaSegura"
}
```

- **cpf**: CPF do passageiro, usado para identificação.
- **senha**: Senha do passageiro.

**Resposta do Servidor:**

- Se o login for bem-sucedido:

  ```python
  "Login bem-sucedido"
  ```

- Se a senha estiver incorreta:

  ```python
  "Senha incorreta"
  ```

- Se o passageiro não estiver cadastrado:

  ```python
  "Novo usuário"
  ```

  O cliente, então, envia uma mensagem de cadastro.

##### Mensagem de Cadastro:

**Mensagem do Cliente:**

```python
{
    "action": "cadastro",
    "cpf": "12345678900",
    "senha": "senhaSegura",
    "nome": "Nome do Passageiro"
}
```

**Resposta do Servidor:**

```python
"Cadastro e login bem-sucedidos"
```

##### 2. **Listar Voos**

O cliente solicita a lista de todos os voos disponíveis no sistema.

**Mensagem do Cliente:**

```python
{
    "action": "listar_voos"
}
```

**Resposta do Servidor:**

```python
[
    (1, "Belém", "Fortaleza"),
    (2, "Fortaleza", "São Paulo"),
    (3, "São Paulo", "Rio de Janeiro"),
    ...
]
```

Cada tupla contém:

- **ID do Voo**: Identificador único do voo.
- **Local de Saída**: Cidade de origem.
- **Local de Destino**: Cidade de destino.

##### 3. **Listar Vagas Disponíveis**

O cliente solicita as vagas disponíveis em um voo específico.

**Mensagem do Cliente:**

```python
{
    "action": "listar_vagas",
    "voo_id": 1
}
```

- **voo_id**: O ID do voo para o qual o cliente deseja consultar as vagas.

**Resposta do Servidor:**

```python
[
    ("1", "disponivel"),
    ("2", "disponivel"),
    ("3", "reservado"),
    ...
]
```

Cada tupla contém:

- **Assento**: Número do assento.
- **Status**: "disponivel" ou "reservado".

##### 4. **Reservar Vaga**

O cliente solicita a reserva de um assento específico em um voo.

**Mensagem do Cliente:**

```python
{
    "action": "reservar_vaga",
    "voo_id": 1,
    "assento": "1"
}
```

- **voo_id**: ID do voo.
- **assento**: Número do assento a ser reservado.

**Resposta do Servidor:**

- Se a reserva for bem-sucedida:

  ```python
  "Assento 1 reservado com sucesso."
  ```

- Se o assento não estiver disponível:

  ```python
  "Assento indisponível ou não encontrado."
  ```

#### Sequência de Mensagens

A sequência de mensagens geralmente segue esta ordem:

1. O cliente realiza o **login** ou **cadastro**.
2. O cliente solicita a **listagem de voos** disponíveis.
3. O cliente seleciona um voo e solicita a **listagem de vagas** disponíveis.
4. O cliente seleciona uma vaga e realiza a **reserva de assento**.

Esse protocolo garante que o cliente possa navegar pelas opções de voos, consultar assentos e finalizar a reserva de maneira eficiente, com respostas estruturadas para cada operação.

## Formatação e Tratamento de Dados

A formatação dos dados transmitidos utiliza a serialização com `pickle`, permitindo a transmissão de estruturas de dados complexas do Python. Para garantir a entrega completa das mensagens, foi implementado um protocolo de comunicação com prefixo de tamanho:

- **Envio de Mensagens (`send_msg`)**: As mensagens são serializadas com `pickle`, e um prefixo de 4 bytes contendo o tamanho da mensagem é adicionado antes do envio.

- **Recebimento de Mensagens (`recv_msg`)**: O receptor lê primeiro os 4 bytes iniciais para determinar o tamanho da mensagem e, em seguida, lê exatamente esse número de bytes para obter a mensagem completa.

Esse mecanismo assegura que as mensagens sejam recebidas integralmente, evitando problemas de dados incompletos ou corrompidos.

## Tratamento de Conexões Simultâneas

O sistema permite a realização de compras de passagens de forma paralela ou simultânea. Para otimizar o paralelismo, o servidor utiliza **threads**, criando uma nova thread para cada conexão de cliente. Isso permite que múltiplos clientes sejam atendidos simultaneamente, melhorando o desempenho e a escalabilidade do sistema.

## Tratamento de Concorrência

Para garantir a integridade dos dados em operações concorrentes, foram utilizados mecanismos de sincronização:

- **Locks**: Foram criados locks (`Lock`) para proteger o acesso às listas compartilhadas de voos e passageiros. Sempre que uma thread precisa acessar ou modificar essas listas, ela adquire o lock correspondente, garantindo exclusão mútua.

- **Exemplo de Uso de Locks**:

  ```python
  with passageiros_lock:
      # Operações seguras na lista de passageiros
      passageiros.append(novo_passageiro)
  ```

Esse tratamento evita condições de corrida e garante que os dados não sejam corrompidos por acessos simultâneos.

## Desempenho e Avaliação

O sistema utiliza threads para melhorar o tempo de resposta e locks para garantir a integridade dos dados. Foram realizados testes práticos com múltiplos clientes simultâneos utilizando o script `test_client.py`, que simula conexões simultâneas e perda de conexão. Os resultados mostraram que o sistema é capaz de atender várias requisições ao mesmo tempo sem comprometer a consistência dos dados.

## Confiabilidade da Solução

A solução implementa mecanismos para melhorar a confiabilidade em cenários de falha de conexão entre o cliente e o servidor:

- **Reconexão Automática**: O cliente inclui lógica de reconexão automática, tentando se conectar novamente ao servidor em caso de falhas temporárias na rede.

- **Tratamento de Exceções**: O servidor e o cliente foram equipados com tratamento de exceções para lidar com erros inesperados sem interromper o funcionamento do sistema.

- **Simulação de Perda de Conexão**: O `test_client.py` simula perdas de conexão abruptas para testar a robustez do servidor em lidar com desconexões inesperadas.

Essas medidas aumentam a robustez do sistema, garantindo que ele continue operando corretamente mesmo em condições adversas.

## Documentação do Código

O código foi escrito de forma clara e estruturada, com nomes de variáveis, funções e classes que refletem suas responsabilidades. Além disso, comentários foram adicionados em trechos complexos para auxiliar na compreensão. Funções principais, como `send_msg`, `recv_msg`, `handle_client`, e as classes dos modelos, estão bem documentadas.

## Emprego do Docker

Utilizamos o **Docker** para contêinerizar o servidor e os clientes, facilitando a implantação e a execução do sistema em diferentes ambientes. O uso do `docker-compose` permite orquestrar múltiplos contêineres de clientes e o servidor de forma simples, simulando um ambiente com vários usuários interagindo simultaneamente.

### Arquivo `docker-compose.yml`

O `docker-compose.yml` define os serviços:

- **Servidor**: Inicia o `server.py` e expõe a porta 8082.
- **Cliente**: Inicia o `client.py` para interação manual.
- **Test_Client**: Inicia o `test_client.py` para testes automatizados.

Exemplo de trecho do `docker-compose.yml`:

```yaml
test_client:
  build:
    context: ./cliente
    dockerfile: Dockerfile
  depends_on:
    - server
  networks:
    voos_network:
      ipv4_address: 172.16.238.13
  environment:
    - SERVER_IP=172.16.238.10
    - PYTHONUNBUFFERED=1
  command: python3 -u test_client.py
```

## Executando o Sistema

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/seu-usuario/pbl_redes_aeroporto.git
    cd pbl_redes_aeroporto
    ```

2. **Construa as imagens Docker**:

    ```bash
    docker-compose build
    ```

3. **Inicie os serviços** (servidor, cliente e teste de clientes):

    ```bash
    docker-compose up
    ```

4. **Acesse os logs do cliente ou do servidor** para visualizar as interações:

    ```bash
    docker-compose logs -f client1
    docker-compose logs -f server
    docker-compose logs -f test_client
    ```

5. **Interaja com o cliente manualmente**:

    Abra um novo terminal e execute:

    ```bash
    docker attach project-root-client1-1
    
    ```
    Aperte enter para iniciar a interação

## Conclusão

Este projeto demonstrou a construção de um sistema distribuído cliente-servidor para uma companhia aérea low-cost, utilizando sockets TCP/IP com mensagens prefixadas, threads para concorrência e contêineres Docker para implantação. Abordamos os desafios de comunicação, concorrência e paralelismo, implementando soluções para garantir a integridade dos dados e a eficiência do sistema. O sistema mostrou-se robusto e escalável, capaz de lidar com múltiplas conexões simultâneas e situações de perda de conexão. Embora haja espaço para melhorias, especialmente em termos de persistência de dados e segurança, o sistema atende aos requisitos básicos e serve como base para desenvolvimentos futuros.

## Referências

- [Documentação do Python - Módulo socket](https://docs.python.org/3/library/socket.html)
- [Documentação do Python - Módulo threading](https://docs.python.org/3/library/threading.html)
- [Documentação do Python - Módulo struct](https://docs.python.org/3/library/struct.html)
- [Docker Documentation](https://docs.docker.com)
- [Python Pickle Module](https://docs.python.org/3/library/pickle.html)
