# Sistema de Compra de Passagens Aéreas - Projeto PBL Redes

Este relatório documenta o **Sistema de Compra de Passagens Aéreas**, desenvolvido como parte da disciplina de Redes e Sistemas Distribuídos. O sistema implementa uma arquitetura cliente-servidor para uma companhia aérea low-cost, permitindo a consulta e compra de passagens de voos disponíveis.

## Equipe de Desenvolvimento

- **Felipe Freitas Alves**
- **Israel Vítor Barreto de Oliveira**

## Arquitetura da Solução

A arquitetura do sistema foi desenvolvida utilizando o modelo cliente-servidor, com comunicação baseada em sockets TCP e troca de mensagens serializadas com o módulo **pickle** do Python. Os componentes e seus papéis na arquitetura são:

- **Servidor** (`server.py`): Responsável por gerenciar os recursos do sistema, como voos, vagas e passageiros. Ele lida com múltiplas conexões de clientes simultaneamente, utilizando threads para cada conexão. O servidor mantém o estado das sessões dos passageiros durante a interação e utiliza mecanismos de sincronização para garantir a integridade dos dados em um ambiente multithread.

- **Clientes** (`client.py`): Aplicações que permitem aos passageiros interagir com o sistema, realizando operações como login, consulta de voos e reserva de assentos. Cada cliente é executado em um contêiner Docker separado para simular usuários distintos.

- **Modelos** (`Models/`): Contém as classes que representam as entidades do sistema:
  - `Voo.py`: Representa um voo, contendo informações como ID, data, local de saída e destino, e uma lista de vagas.
  - `Vaga.py`: Representa uma vaga (assento) em um voo, incluindo status e métodos para reservar o assento.
  - `Passageiro.py`: Representa um passageiro, com dados pessoais e autenticação.

## Paradigma de Comunicação

O paradigma de serviço utilizado é o **stateful**. O servidor mantém o estado da sessão de cada passageiro após o login, permitindo que ele realize múltiplas operações sem a necessidade de reautenticação. Essa escolha foi motivada pela necessidade de manter informações de contexto durante as interações, proporcionando uma experiência mais consistente e personalizada para o usuário.

### Protocolo de Comunicação

O protocolo de comunicação entre o cliente e o servidor no **Sistema de Compra de Passagens Aéreas** foi desenvolvido utilizando sockets TCP e mensagens serializadas com o módulo **pickle** do Python. Esse protocolo garante a troca de informações de forma estruturada, permitindo que operações como login, listagem de voos, consulta de vagas e reservas de assentos sejam realizadas com segurança e eficiência.

#### Estrutura das Mensagens

As mensagens trocadas entre o cliente e o servidor são dicionários Python serializados com o **pickle**. Cada mensagem inclui um campo de **ação** e dados específicos para cada operação.

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
- **nome**, **data_nasc**, **endereco**: Dados enviados apenas no primeiro login (caso o passageiro não esteja cadastrado).

**Resposta do Servidor:**

- Se o login for bem-sucedido:

```python
"Login bem-sucedido"
```

- Se a senha estiver incorreta:

```python
"Senha incorreta"
```

- Se o passageiro não estiver cadastrado (novo usuário):

```python
"Novo usuário"
```

O cliente, ao receber "Novo usuário", envia os dados adicionais para cadastro:

```python
{
    "action": "login",
    "cpf": "12345678900",
    "senha": "senhaSegura",
}
```

E o servidor responde:

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
    (2, "Fortaleza", "São Paulo")
]
```

Cada tupla representa um voo com seu ID, local de saída e local de destino.

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

Se o voo for encontrado:

```python
[
    ("1A", "disponivel"),
    ("1B", "disponivel")
]
```

Se o voo não for encontrado:

```python
"Voo não encontrado"
```

##### 4. **Reservar Vaga**

O cliente solicita a reserva de um assento específico em um voo.

**Mensagem do Cliente:**

```python
{
    "action": "reservar_vaga",
    "voo_id": 1,
    "assento": "1A"
}
```

- **voo_id**: ID do voo.
- **assento**: Número do assento a ser reservado.

**Resposta do Servidor:**

- Se a reserva for bem-sucedida:

```python
"Assento 1A reservado com sucesso."
```

- Se o assento não estiver disponível ou não for encontrado:

```python
"Assento indisponível ou não encontrado."
```

#### Sequência de Mensagens

A sequência de mensagens geralmente segue esta ordem:

1. O cliente realiza o **login** ou **cadastro**.
2. O cliente solicita a **listagem de voos** disponíveis.
3. O cliente seleciona um voo e solicita a **listagem de vagas** disponíveis.
4. O cliente seleciona uma vaga e realiza a **reserva de assento**.

Esse protocolo garante que o cliente possa navegar pelas opções de voos, consultar assentos e finalizar a reserva de maneira eficiente.

## Formatação e Tratamento de Dados

A formatação dos dados transmitidos utiliza o módulo **pickle** do Python, que serializa objetos Python em um formato binário. Embora o uso do pickle seja eficiente dentro de um ambiente controlado, é importante notar que ele não é seguro contra dados maliciosos e não deve ser usado com dados não confiáveis. No contexto deste projeto, onde tanto o cliente quanto o servidor estão sob nosso controle, o uso do pickle simplifica a serialização e desserialização de objetos complexos.

## Tratamento de Conexões Simultâneas

O sistema permite a realização de compras de passagens de forma paralela ou simultânea. Para otimizar o paralelismo, o servidor utiliza **threads**, criando uma nova thread para cada conexão de cliente. Isso permite que múltiplos clientes sejam atendidos simultaneamente, melhorando o desempenho e a escalabilidade do sistema.

## Tratamento de Concorrência

Para garantir a integridade dos dados em um ambiente multithread, foram implementados mecanismos de sincronização utilizando o módulo `threading.Lock` do Python. Locks são utilizados para proteger o acesso aos recursos compartilhados, como as listas de voos e passageiros.

- **Locks Implementados:**
  - `voos_lock`: Protege o acesso à lista de voos (`voos`).
  - `passageiros_lock`: Protege o acesso à lista de passageiros (`passageiros`).

Sempre que uma thread (cliente) precisa acessar ou modificar esses recursos, ela adquire o lock correspondente antes de realizar a operação, garantindo que apenas uma thread por vez possa modificar os dados compartilhados.

Exemplo de uso:

```python
with passageiros_lock:
    passageiro = next((p for p in passageiros if p.cpf == cpf), None)
```

## Desempenho e Avaliação

O sistema utiliza **threads** para melhorar o tempo de resposta e **locks** para garantir a integridade dos dados. Foram realizados testes práticos com múltiplos clientes simultâneos para avaliar o comportamento do sistema. Os resultados mostraram que o sistema é capaz de atender várias requisições ao mesmo tempo sem comprometer a consistência dos dados. A sincronização com locks introduz um pequeno overhead, mas é essencial para evitar condições de corrida.

## Confiabilidade da Solução

A solução implementa mecanismos para melhorar a confiabilidade em cenários de falha de conexão entre o cliente e o servidor. A lógica de reconexão automática foi adicionada ao cliente, garantindo que, caso a conexão com o servidor seja perdida, o cliente tentará se reconectar automaticamente até um número máximo de tentativas.

No **cliente**, a função `connect_with_retry` tenta estabelecer a conexão com o servidor, realizando múltiplas tentativas com intervalos de espera definidos. Isso melhora a robustez do sistema em cenários de falhas temporárias na rede ou reinicialização do servidor.

## Documentação do Código

O código foi escrito de forma **autoexplicativa**, com nomes de variáveis, funções e classes que refletem claramente suas responsabilidades. Além disso, comentários foram adicionados em trechos complexos para auxiliar na compreensão.

## Emprego do Docker

Utilizamos o **Docker** para contêinerizar o servidor e os clientes, facilitando a implantação e a execução do sistema em diferentes ambientes. O uso do `docker-compose` permite orquestrar múltiplos contêineres de clientes e o servidor de forma simples, simulando um ambiente com vários usuários interagindo simultaneamente.

Cada serviço (servidor e clientes) possui seu próprio Dockerfile, e o `docker-compose.yml` configura a rede, os endereços IP fixos e as dependências entre os serviços.

## Executando o Sistema

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passo a Passo

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/pbl_redes_aeroporto.git
    cd pbl_redes_aeroporto
    ```

2. **Construa as imagens Docker:**

    ```bash
    docker-compose build
    ```

3. **Inicie os serviços:**

    ```bash
    docker-compose up
    ```

4. **Acesse os clientes:**

    Como os clientes estão configurados para permitir interação (`stdin_open: true` e `tty: true`), você pode acessar os terminais dos clientes em janelas separadas.

    Em um novo terminal, execute:

    ```bash
    docker attach pbl_redes_aeroporto_client1_1
    ```

    E em outro terminal:

    ```bash
    docker attach pbl_redes_aeroporto_client2_1
    ```

    *Substitua `pbl_redes_aeroporto` pelo nome do seu projeto ou pelo nome dado ao contêiner.*

5. **Interaja com os clientes:**

    Agora você pode interagir com os clientes, fazer login, listar voos, reservar vagas, etc.

6. **Parar os serviços:**

    Quando terminar os testes, você pode parar os contêineres com:

    ```bash
    docker-compose down
    ```

## Conclusão

Este projeto demonstrou a construção de um sistema distribuído cliente-servidor para uma companhia aérea low-cost, utilizando sockets TCP/IP, threads para concorrência e contêineres Docker para implantação. Abordamos os desafios de comunicação, concorrência e paralelismo, implementando soluções para garantir a integridade dos dados e a eficiência do sistema.

A utilização do módulo **pickle** para serialização facilitou o desenvolvimento, embora em aplicações reais seja recomendável o uso de protocolos mais seguros e padronizados, como JSON ou Protobuf.

Implementamos mecanismos de sincronização para evitar condições de corrida em um ambiente multithread e adicionamos lógica de reconexão para aumentar a robustez do sistema.

## Referências

- [Documentação do Python - Módulo socket](https://docs.python.org/3/library/socket.html)
- [Documentação do Python - Módulo threading](https://docs.python.org/3/library/threading.html)
- [Documentação do Python - Módulo pickle](https://docs.python.org/3/library/pickle.html)
- [Docker Documentation](https://docs.docker.com)