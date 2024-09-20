# Sistema de Compra de Passagens Aéreas - Projeto PBL Redes

Este repositório contém o código-fonte e a documentação do projeto **Sistema de Compra de Passagens Aéreas**, desenvolvido como parte da disciplina de Redes e Sistemas Distribuídos. O sistema implementa uma arquitetura cliente-servidor baseada em TCP/IP para uma companhia aérea low-cost, permitindo a consulta e compra de passagens de voos disponíveis.

## Equipe de Desenvolvimento
- **Nome do Aluno 1** - FELIPE FREITAS ALVES
- **Nome do Aluno 2** - ISRAEL VÍTOR BARRETO DE OLIVEIRA

## Descrição do Sistema

Este sistema foi desenvolvido para simular o funcionamento de um sistema de compra de passagens aéreas onde múltiplos clientes podem consultar voos e reservar assentos em tempo real, utilizando comunicação via sockets TCP.

### Funcionalidades Principais
- **Login e Cadastro de Passageiros**: Os clientes podem fazer login utilizando CPF e senha. Caso o passageiro não esteja cadastrado, ele será registrado automaticamente.
- **Consulta de Voos**: Os clientes podem listar todos os voos disponíveis no sistema.
- **Consulta de Vagas**: Cada cliente pode consultar as vagas disponíveis para um voo específico.
- **Reserva de Assentos**: O cliente pode reservar um assento disponível em um voo. O sistema garante que o primeiro cliente a reservar um assento tenha preferência.

## Arquitetura do Sistema

O sistema é composto por duas partes principais:
1. **Servidor**: Gerencia o estado central do sistema, incluindo voos, passageiros e vagas. Ele lida com as conexões dos clientes de forma concorrente usando threads.
2. **Clientes**: Interagem com o servidor para realizar consultas e reservas de passagens. Cada cliente é executado em um contêiner Docker separado para simular múltiplos usuários.

### Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada para o desenvolvimento tanto do servidor quanto dos clientes.
- **Sockets TCP/IP**: Para comunicação entre o cliente e o servidor, utilizando a API nativa de sockets do Python.
- **Docker**: Utilizado para facilitar o teste do sistema com múltiplos clientes e servidores, isolando os ambientes de execução.
- **Pickle**: Usado para serialização e desserialização dos dados transmitidos entre cliente e servidor.

## Estrutura de Arquivos

- **/GerenciadorDeVoos/**: Contém os arquivos de código-fonte do sistema:
  - `client.py`: Código do cliente que se conecta ao servidor e realiza as operações de consulta e compra.
  - `server.py`: Código do servidor que gerencia as requisições dos clientes.
  - **/Models/**: Contém as classes que modelam os voos, vagas, passageiros e passagens:
    - `Voo.py`: Classe que representa um voo.
    - `Vaga.py`: Classe que representa uma vaga (assento) em um voo.
    - `Passageiro.py`: Classe que representa um passageiro.
    - `Passagem.py`: Classe que representa uma passagem emitida para um passageiro.

- **Dockerfile.client**: Arquivo Dockerfile para a construção da imagem do cliente.
- **Dockerfile.server**: Arquivo Dockerfile para a construção da imagem do servidor.
- **docker-compose.yml**: Arquivo de orquestração que configura e executa os contêineres de servidor e múltiplos clientes.

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

3. **Inicie os serviços** (1 servidor e 10 clientes):

    ```bash
    docker-compose up
    ```

4. **Acesse os logs do cliente ou do servidor** para visualizar as interações:

    ```bash
    docker-compose logs client1
    docker-compose logs server
    ```

## Escolhas Técnicas

### Comunicação via TCP/IP

Optamos por utilizar o protocolo TCP/IP para garantir a confiabilidade na comunicação entre clientes e servidor, assegurando que todas as mensagens sejam entregues e processadas na ordem correta.

A API de sockets nativa do Python foi utilizada para implementar essa comunicação. As mensagens entre cliente e servidor são serializadas com o módulo `pickle`, que facilita a transmissão de estruturas de dados complexas (como dicionários).

### Concorrência no Servidor

Para lidar com múltiplos clientes simultâneos, o servidor utiliza threads, onde cada conexão de cliente é gerida por uma thread separada. Isso permite que o servidor possa atender vários pedidos de forma concorrente, simulando o comportamento de um sistema real com múltiplos usuários acessando ao mesmo tempo.

### Contêineres Docker

Para facilitar o teste e execução do sistema com múltiplos clientes, utilizamos o Docker. O `docker-compose` permite a orquestração de um ambiente com um servidor e múltiplos clientes, todos isolados e funcionando de maneira independente.

### Serialização de Dados

O uso do módulo `pickle` para serializar e desserializar os dados transmitidos entre o cliente e o servidor foi escolhido pela simplicidade e compatibilidade com o Python. Essa abordagem nos permitiu transmitir objetos complexos como dicionários e listas de maneira eficiente.

## Testes e Validação

O sistema foi testado em ambiente Docker com múltiplas instâncias de clientes e um servidor. As funcionalidades de login, listagem de voos e reserva de assentos foram validadas. O sistema respondeu corretamente às solicitações concorrentes, garantindo que o primeiro cliente a reservar um assento tenha preferência.

## Conclusão

Este projeto demonstrou a viabilidade de construir um sistema distribuído cliente-servidor para uma companhia aérea low-cost, utilizando tecnologias como sockets TCP/IP e contêineres Docker. A implementação permite que clientes realizem consultas e reservas de passagens em um ambiente concorrente, respeitando as exigências de confiabilidade e escalabilidade.

## Referências

- Documentação do Python (https://docs.python.org/3/library/socket.html)
- Docker Documentation (https://docs.docker.com)
