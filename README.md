# Sistema de Compra de Passagens Aéreas - Projeto PBL Redes

Este relatório documenta o **Sistema de Compra de Passagens Aéreas**, desenvolvido como parte da disciplina de Redes e Sistemas Distribuídos. O sistema implementa uma arquitetura cliente-servidor para uma companhia aérea low-cost, permitindo a consulta e compra de passagens de voos disponíveis.

## Equipe de Desenvolvimento

- **Felipe Freitas Alves**
- **Israel Vítor Barreto de Oliveira**

## Arquitetura da Solução

A arquitetura do sistema foi desenvolvida utilizando o modelo cliente-servidor, com comunicação baseada em sockets TCP e troca de mensagens em formato JSON. Os componentes e seus papéis na arquitetura são:

- **Servidor** (`server.py`): Responsável por gerenciar os recursos do sistema, como voos, vagas e passageiros. Ele lida com múltiplas conexões de clientes simultaneamente, utilizando threads para cada conexão. O servidor mantém o estado das sessões dos passageiros durante a interação.
  
- **Clientes** (`client.py`): Aplicações que permitem aos passageiros interagir com o sistema, realizando operações como login, consulta de voos e reserva de assentos. Cada cliente é executado em um contêiner Docker separado para simular usuários distintos.

- **Modelos** (`Models/`): Contém as classes que representam as entidades do sistema:
  - `Voo.py`: Representa um voo, contendo informações como ID, data, local de saída e destino.
  - `Vaga.py`: Representa uma vaga (assento) em um voo, incluindo status e controle de concorrência.
  - `Passageiro.py`: Representa um passageiro, com dados pessoais e autenticação.
  - `Passagem.py`: Representa uma passagem emitida para um passageiro específico.

## Paradigma de Comunicação

O paradigma de serviço utilizado é o **stateful**. O servidor mantém o estado da sessão de cada passageiro após o login, permitindo que ele realize múltiplas operações sem a necessidade de reautenticação. Essa escolha foi motivada pela necessidade de manter informações de contexto durante as interações, proporcionando uma experiência mais consistente e personalizada para o usuário.

### Protocolo de Comunicação

O protocolo de comunicação entre o cliente e o servidor no **Sistema de Compra de Passagens Aéreas** foi desenvolvido utilizando sockets TCP e mensagens em formato **JSON**. Esse protocolo garante a troca de informações de forma estruturada, permitindo que operações como login, listagem de voos, consulta de vagas e reservas de assentos sejam realizadas com segurança e eficiência.

#### Estrutura das Mensagens

As mensagens trocadas entre o cliente e o servidor seguem uma estrutura padronizada em JSON, que inclui um campo de **ação** e dados específicos para cada operação. Abaixo estão as mensagens enviadas e recebidas entre os componentes do sistema:

##### 1. **Login de Passageiro**
O cliente envia os dados de login ou cadastro do passageiro.

**Mensagem do Cliente:**
```json
{
    "action": "login",
    "cpf": "12345678900",
    "senha": "senhaSegura",
    "nome": "João Silva",
    "data_nasc": "1990-01-01",
    "endereco": "Rua A, 123"
}
```
- **cpf**: CPF do passageiro, usado para identificação.
- **senha**: Senha do passageiro (hashed no servidor).
- **nome**, **data_nasc**, **endereco**: Dados enviados apenas no primeiro login (caso o passageiro não esteja cadastrado).

**Resposta do Servidor:**
```json
"Login bem-sucedido"
```
Ou, caso as credenciais estejam incorretas:
```json
"Senha incorreta"
```
Se o passageiro for novo e for cadastrado:
```json
"Cadastro e login bem-sucedidos"
```

##### 2. **Listar Voos**
O cliente solicita a lista de todos os voos disponíveis no sistema.

**Mensagem do Cliente:**
```json
{
    "action": "listar_voos"
}
```

**Resposta do Servidor:**
```json
[
    {
        "id_voo": 1,
        "local_saida": "Belém",
        "local_destino": "Fortaleza"
    },
    {
        "id_voo": 2,
        "local_saida": "Fortaleza",
        "local_destino": "São Paulo"
    }
]
```

##### 3. **Listar Vagas Disponíveis**
O cliente solicita as vagas disponíveis em um voo específico.

**Mensagem do Cliente:**
```json
{
    "action": "listar_vagas",
    "voo_id": 1
}
```
- **voo_id**: O ID do voo para o qual o cliente deseja consultar as vagas.

**Resposta do Servidor:**
```json
[
    {
        "assento": "1A",
        "status": "disponivel"
    },
    {
        "assento": "1B",
        "status": "disponivel"
    }
]
```

##### 4. **Reservar Vaga**
O cliente solicita a reserva de um assento específico em um voo.

**Mensagem do Cliente:**
```json
{
    "action": "reservar_vaga",
    "voo_id": 1,
    "assento": "1A"
}
```
- **voo_id**: ID do voo.
- **assento**: Número do assento a ser reservado.

**Resposta do Servidor:**
```json
"Assento 1A reservado com sucesso."
```
Ou, caso o assento não esteja disponível:
```json
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

Essa seção fornece uma descrição completa do protocolo de comunicação usado no projeto e pode ser integrada ao relatório principal.

### Mensagens e Ordem das Mensagens Trocadas

1. **Login ou Cadastro**:
   - **Cliente envia**: `{ "action": "login", "cpf": "...", "senha": "...", "nome": "...", "data_nasc": "...", "endereco": "..." }`
   - **Servidor responde**: Confirmação de login ou cadastro bem-sucedido.

2. **Listar Voos**:
   - **Cliente envia**: `{ "action": "listar_voos" }`
   - **Servidor responde**: Lista de voos disponíveis.

3. **Listar Vagas**:
   - **Cliente envia**: `{ "action": "listar_vagas", "voo_id": ... }`
   - **Servidor responde**: Lista de vagas disponíveis para o voo selecionado.

4. **Reservar Vaga**:
   - **Cliente envia**: `{ "action": "reservar_vaga", "voo_id": ..., "assento": "..." }`
   - **Servidor responde**: Confirmação de reserva ou mensagem de erro.

## Formatação e Tratamento de Dados

A formatação dos dados transmitidos utiliza o formato **JSON**, que é amplamente suportado e facilita a interoperabilidade entre sistemas e linguagens diferentes. Isso permite que, no futuro, clientes desenvolvidos em outras linguagens possam se integrar facilmente ao sistema. Além disso, o uso de JSON torna as mensagens legíveis e facilita o debug.

## Tratamento de Conexões Simultâneas

O sistema permite a realização de compras de passagens de forma paralela ou simultânea. Para otimizar o paralelismo, o servidor utiliza **threads**, criando uma nova thread para cada conexão de cliente. Isso permite que múltiplos clientes sejam atendidos simultaneamente, melhorando o desempenho e a escalabilidade do sistema.

## Tratamento de Concorrência

Criamos um threading.Lock() chamado global_lock, que será usado para proteger o acesso à lista de passageiros. Esse lock será compartilhado entre todas as threads.

Sempre que uma thread precisar acessar ou modificar a lista de passageiros (como durante login ou cadastro), o lock será adquirido antes de realizar a operação. Isso garante que apenas uma thread por vez possa acessar a lista, prevenindo condições de corrida e problemas de concorrência.

A inclusão do lock global protege a lista de passageiros de acessos simultâneos, garantindo que os dados não sejam corrompidos por modificações concorrentes de múltiplos clientes.

## Desempenho e Avaliação

O sistema utiliza **threads** para melhorar o tempo de resposta e **locks** para garantir a integridade dos dados. Embora não tenham sido realizados testes de desempenho formais, fizemos testes práticos com múltiplos clientes simultâneos para avaliar o comportamento do sistema. Os resultados mostraram que o sistema é capaz de atender várias requisições ao mesmo tempo sem comprometer a consistência dos dados.

## Confiabilidade da Solução

A solução implementa mecanismos para melhorar a confiabilidade em cenários de falha de conexão entre o cliente e o servidor. A lógica de reconexão automática foi adicionada ao cliente, garantindo que, caso a conexão com o servidor seja perdida, o cliente tentará se reconectar automaticamente até um número máximo de tentativas.

O cliente foi configurado para detectar desconexões (como falha de rede ou servidor offline) e automaticamente iniciar um processo de reconexão. Se a conexão for perdida durante uma operação, o cliente tenta se reconectar ao servidor e continuar a comunicação. O cliente realiza até 5 tentativas de reconexão, com um intervalo de 3 segundos entre cada tentativa. Após a reconexão, a última mensagem que estava sendo enviada é retransmitida para garantir que a operação seja concluída.

Caso a conexão seja perdida, o socket é fechado corretamente antes de iniciar o processo de reconexão. Isso evita problemas de recursos bloqueados e possíveis falhas durante o processo de reconexão.

A reconexão automática melhora a robustez do sistema em cenários de falhas temporárias na rede ou reinicialização do servidor. No entanto, caso o servidor fique offline por um longo período, o cliente desistirá após o número máximo de tentativas de reconexão, o que garante que o cliente não fique preso em um loop infinito de tentativas.

## Documentação do Código

O código foi escrito de forma **autoexplicativa**, com nomes de variáveis, funções e classes que refletem claramente suas responsabilidades. Além disso, comentários foram adicionados em trechos complexos para auxiliar na compreensão.

## Emprego do Docker

Utilizamos o **Docker** para contêinerizar o servidor e os clientes, facilitando a implantação e a execução do sistema em diferentes ambientes. O uso do `docker-compose` permite orquestrar múltiplos contêineres de clientes e o servidor de forma simples, simulando um ambiente com vários usuários interagindo simultaneamente.

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

3. **Inicie os serviços** (1 servidor e múltiplos clientes):

    ```bash
    docker-compose up
    ```

4. **Acesse os logs do cliente ou do servidor** para visualizar as interações:

    ```bash
    docker-compose logs client1
    docker-compose logs server
    ```

## Conclusão

Este projeto demonstrou a construção de um sistema distribuído cliente-servidor para uma companhia aérea low-cost, utilizando sockets TCP/IP, threads para concorrência e contêineres Docker para implantação. Abordamos os desafios de comunicação, concorrência e paralelismo, implementando soluções para garantir a integridade dos dados e a eficiência do sistema. Embora haja espaço para melhorias, especialmente em termos de confiabilidade e persistência, o sistema atende aos requisitos básicos e serve como base para desenvolvimentos futuros.

## Referências

- [Documentação do Python - Módulo socket](https://docs.python.org/3/library/socket.html)
- [Documentação do Python - Módulo threading](https://docs.python.org/3/library/threading.html)
- [Formato JSON](https://www.json.org/json-pt.html)
- [Docker Documentation](https://docs.docker.com)