import socket
import pickle
import os
import time
import struct

SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = 8082

MAX_RETRIES = 5
RETRY_DELAY = 5  # segundos entre as tentativas de conexão

def send_msg(sock, msg):
    """Envia uma mensagem prefixada com seu tamanho."""
    data = pickle.dumps(msg)
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)

def recv_msg(sock):
    """Recebe uma mensagem prefixada com seu tamanho."""
    # Primeiro, lê os 4 bytes que representam o tamanho
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Então, lê a quantidade exata de bytes da mensagem
    data = recvall(sock, msglen)
    if data is None:
        return None
    return pickle.loads(data)

def recvall(sock, n):
    """Função auxiliar para receber n bytes ou retornar None se EOF for atingido."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def login(sock):
    input("\nPressione Enter para continuar...")
    print("\nFaça login ou cadastre-se:")
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    request = {'action': 'login', 'cpf': cpf, 'senha': senha}
    send_msg(sock, request)
    response = recv_msg(sock)
    if response == "Senha incorreta":
        print("Senha incorreta. Tente novamente.")
        return False
    elif response == "Login bem-sucedido":
        print("Login bem-sucedido!")
        return True
    elif response == "Novo usuário":
        nome = input("Digite seu nome: ")
        request = {
            'action': 'cadastro',
            'cpf': cpf,
            'senha': senha,
            'nome': nome
        }
        send_msg(sock, request)
        response = recv_msg(sock)
        if response == "Cadastro e login bem-sucedidos":
            print("Cadastro e login bem-sucedidos!")
            return True
        else:
            print("Falha no cadastro. Tente novamente.")
            return False
    else:
        print("Erro desconhecido.")
        return False

def connect_with_retry(host, port, retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Tenta se conectar ao servidor com várias tentativas."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for attempt in range(1, retries + 1):
        try:
            print(f"Tentando se conectar ao servidor {host}:{port}... (Tentativa {attempt}/{retries})")
            sock.connect((host, port))
            print(f"Conexão estabelecida com {host}:{port}")
            return sock
        except (ConnectionRefusedError, OSError) as e:
            print(f"Erro ao conectar: {e}")
            if attempt < retries:
                print(f"Aguardando {delay} segundos antes de tentar novamente...")
                time.sleep(delay)
            else:
                print("Número máximo de tentativas atingido. Não foi possível conectar ao servidor.")
                raise
    return None

def client(host=SERVER_IP, port=SERVER_PORT):
    # Tentar se conectar com retries
    sock = connect_with_retry(host, port)

    if sock is None:
        print("Encerrando o cliente por falta de conexão.")
        return

    logged_in = False
    while not logged_in:
        logged_in = login(sock)

    try:
        while True:

            print("\nEscolha uma ação:")
            print("1. Listar voos")
            print("2. Listar vagas de um voo")
            print("3. Reservar uma vaga")
            print("4. Sair")
            escolha = input("Digite o número da ação desejada: ")

            if escolha == '1':
                request = {'action': 'listar_voos'}
                send_msg(sock, request)
                response = recv_msg(sock)
                print("Voos disponíveis:")
                if isinstance(response, list):
                    for voo in response:
                        print(f"ID: {voo[0]}, De: {voo[1]}, Para: {voo[2]}")
                else:
                    print(response)

            elif escolha == '2':
                voo_id = int(input("Digite o ID do voo: "))
                request = {'action': 'listar_vagas', 'voo_id': voo_id}
                send_msg(sock, request)
                response = recv_msg(sock)
                if isinstance(response, str):
                    print(response)
                else:
                    print(f"Vagas disponíveis no voo {voo_id}:")
                    for vaga in response:
                        print(f"Assento: {vaga[0]}, Status: {vaga[1]}")

            elif escolha == '3':
                voo_id = int(input("Digite o ID do voo: "))
                assento = input("Digite o número do assento: ")
                request = {'action': 'reservar_vaga', 'voo_id': voo_id, 'assento': assento}
                send_msg(sock, request)
                response = recv_msg(sock)
                print(response)

            elif escolha == '4':
                request = {'action': 'sair'}
                send_msg(sock, request)
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    finally:
        sock.close()

if __name__ == "__main__":
    client()
