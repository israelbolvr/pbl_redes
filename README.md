# Sistema de Compra de Passagens Aéreas - Projeto PBL Redes

Este relatório documenta o **Sistema de Compra de Passagens Aéreas**, desenvolvido como parte da disciplina de Redes e Sistemas Distribuídos. O sistema implementa uma arquitetura cliente-servidor para uma companhia aérea low-cost, permitindo a consulta e compra de passagens de voos disponíveis.

## Equipe de Desenvolvimento

- **Felipe Freitas Alves**
- **Israel Vítor Barreto de Oliveira**

## Arquitetura da Solução

A arquitetura do sistema foi desenvolvida utilizando o modelo cliente-servidor, com comunicação baseada em sockets TCP e troca de mensagens serializadas com **pickle**. Os componentes e seus papéis na arquitetura são:

- **Servidor** (`server.py`): Responsável por gerenciar os recursos do sistema, como voos, vagas e passageiros. Ele lida com múltiplas conexões de clientes simultaneamente, utilizando threads para cada conexão【22†source】. O servidor mantém o estado das sessões dos passageiros durante a interação.
  
- **Clientes** (`client.py`): Aplicações que permitem aos passageiros interagir com o sistema, realizando operações como login, consulta de voos e reserva de assentos【25†source】. Cada cliente é executado em um contêiner Docker separado para simular usuários distintos.

- **Modelos** (`Models/`): Contém as classes que representam as entidades do sistema:
  - `Voo.py`: Representa um voo, contendo informações como ID, data, local de saída e destino.
  - `Vaga.py`: Representa uma vaga (assento) em um voo, incluindo status e controle de concorrência.
  - `Passageiro.py`: Representa um passageiro, com dados pessoais e autenticação.
  - `Passagem.py`: Representa uma passagem emitida para um passageiro específico.

## Paradigma de Comunicação

O paradigma de serviço utilizado é o **stateful**. O servidor mantém o estado da sessão de cada passageiro após o login, permitindo que ele realize múltiplas operações sem a necessidade de reautenticação. Essa escolha foi motivada pela necessidade de manter informações de contexto durante as interações, proporcionando uma experiência mais consistente e personalizada para o usuário.

### Protocolo de Comunicação

O protocolo de comunicação entre o cliente e o servidor no **Sistema de Compra de Passagens Aéreas** foi desenvolvido utilizando sockets TCP e serialização de mensagens com **pickle**. Esse protocolo garante a troca de informações de forma estruturada, permitindo que operações como login, listagem de voos, consulta de vagas e reservas de assentos sejam realizadas com segurança e eficiência.

#### Estrutura das Mensagens

As mensagens trocadas entre o cliente e o servidor seguem uma estrutura padronizada em objetos Python, que são serializados com `pickle`. Abaixo estão as mensagens enviadas e recebidas entre os componentes do sistema:

##### 1. **Login de Passageiro**
O cliente envia os dados de login ou cadastro do passageiro.

**Mensagem do Cliente:**
```python
{
    'action': 'login',
    'cpf': '12345678900',
    'senha': 'senhaSegura'
}
```
- **cpf**: CPF do passageiro, usado para identificação.
- **senha**: Senha do passageiro.

**Resposta do Servidor:**
```python
"Login bem-sucedido"
```
Ou, caso as credenciais estejam incorretas:
```python
"Senha incorreta"
```
Se o passageiro for novo e for cadastrado:
```python
"Cadastro e login bem-sucedidos"
```

##### 2. **Listar Voos**
O cliente solicita a lista de todos os voos disponíveis no sistema.

**Mensagem do Cliente:**
```python
{
    'action': 'listar_voos'
}
```

**Resposta do Servidor:**
```python
[
    (1, "Belém", "Fortaleza"),
    (2, "Fortaleza", "São Paulo")
]
```

##### 3. **Listar Vagas Disponíveis**
O cliente solicita as vagas disponíveis em um voo específico.

**Mensagem do Cliente:**
```python
{
    'action': 'listar_vagas',
    'voo_id': 1
}
```
- **voo_id**: O ID do voo para o qual o cliente deseja consultar as vagas.

**Resposta do Servidor:**
```python
[
    ("1A", "disponivel"),
    ("1B", "disponivel")
]
```

##### 4. **Reservar Vaga**
O cliente solicita a reserva de um assento específico em um voo.

**Mensagem do Cliente:**
```python
{
    'action': 'reservar_vaga',
    'voo_id': 1,
    'assento': '1A'
}
```
- **voo_id**: ID do voo.
- **assento**: Número do assento a ser reservado.

**Resposta do Servidor:**
```python
"Assento 1A reservado com sucesso."
```
Ou, caso o assento não esteja disponível:
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

---

## Tratamento de Conexões Simultâneas

O sistema permite a realização de compras de passagens de forma paralela ou simultânea. Para otimizar o paralelismo, o servidor utiliza **threads**, criando uma nova thread para cada conexão de cliente【22†source】. Isso permite que múltiplos clientes sejam atendidos simultaneamente, melhorando o desempenho e a escalabilidade do sistema.

## Tratamento de Concorrência

O código atual não implementa uma estratégia explícita para controlar a concorrência entre threads, como um `lock` para operações sensíveis que envolvem a lista de voos e vagas. Isso pode levar a possíveis condições de corrida. Recomenda-se o uso de um **threading.Lock()** para proteger o acesso a recursos compartilhados, como a lista de passageiros e vagas de voos.

## Documentação do Código

O código foi escrito de forma **autoexplicativa**, com nomes de variáveis, funções e classes que refletem claramente suas responsabilidades. Além disso, foram adicionados comentários em trechos mais complexos para auxiliar na compreensão do sistema.

## Dependências

O arquivo `requirements.txt` especifica as dependências do projeto:

- **bcrypt**: Usado para hash de senhas【23†source】【24†source】.

## Emprego do Docker

Utilizamos o **Docker** para contêinerizar o servidor e os clientes, facilitando a implantação e a execução do sistema em diferentes ambientes. O uso do `docker-compose` permite orquestrar múltiplos contêineres de clientes e o servidor de forma simples, simulando um ambiente com vários usuários interagindo simultaneamente.

---

### Conclusão

Este projeto demonstrou a construção de um sistema distribuído cliente-servidor para uma companhia aérea low-cost, utilizando sockets TCP/IP, threads para concorrência e contêineres Docker para implantação. Abordamos os desafios de comunicação, concorrência e paralelismo, implementando soluções para garantir a integridade dos dados e a eficiência do sistema.

### Referências

- [Documentação do Python - Módulo socket](https://docs.python.org/3/library/socket.html)
- [Documentação do Python - Módulo threading](https://docs.python.org/3/library/threading.html)
- [Docker Documentation](https://docs.docker.com)
