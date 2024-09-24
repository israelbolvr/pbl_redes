import socket
import json
import time

MAX_RETRIES = 5  # Número máximo de tentativas de reconexão
RETRY_DELAY = 3  # Intervalo em segundos entre tentativas de reconexão

def connect_to_server(host, port):
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            # Tenta se conectar ao servidor
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print(f"Conectado ao servidor {host}:{port}")
            return client_socket
        except (ConnectionRefusedError, socket.error):
            attempt += 1
            print(f"Falha na conexão. Tentativa {attempt} de {MAX_RETRIES}...")
            time.sleep(RETRY_DELAY)

    print("Falha em conectar ao servidor após várias tentativas.")
    return None

def send_message(client_socket, message):
    try:
        client_socket.sendall(json.dumps(message).encode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        print("Conexão perdida. Tentando reconectar...")
        client_socket = reconnect(client_socket)
        if client_socket:
            client_socket.sendall(json.dumps(message).encode('utf-8'))

def reconnect(client_socket):
    # Fecha o socket existente antes de tentar reconectar
    client_socket.close()

    # Tenta reconectar ao servidor
    return connect_to_server('127.0.0.1', 8082)

def main():
    host = '127.0.0.1'
    port = 8082

    client_socket = connect_to_server(host, port)
    if client_socket is None:
        return  # Se a conexão falhar após várias tentativas, encerra o cliente

    try:
        while True:
            action = input("Digite a ação (login, listar_voos, reservar_vaga): ")

            if action == "login":
                cpf = input("Digite seu CPF: ")
                senha = input("Digite sua senha: ")
                message = {"action": "login", "cpf": cpf, "senha": senha}

            elif action == "listar_voos":
                message = {"action": "listar_voos"}

            elif action == "reservar_vaga":
                voo_id = input("Digite o ID do voo: ")
                assento = input("Digite o número do assento: ")
                message = {"action": "reservar_vaga", "voo_id": int(voo_id), "assento": assento}

            send_message(client_socket, message)

            response = client_socket.recv(4096)
            print(f"Resposta do servidor: {response.decode('utf-8')}")
    except (KeyboardInterrupt, SystemExit):
        print("\nCliente encerrado.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
