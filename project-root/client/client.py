import socket
import json
import time
import os

def login(sock):
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    request = {'action': 'login', 'cpf': cpf, 'senha': senha}
    sock.sendall(json.dumps(request).encode('utf-8'))
    response = json.loads(sock.recv(4096).decode('utf-8'))
    if response == "Senha incorreta":
        print("Senha incorreta. Tente novamente.")
        return False
    elif response == "Login bem-sucedido":
        print("Login bem-sucedido!")
        return True
    elif response == "Cadastro e login bem-sucedidos":
        print("Cadastro e login bem-sucedidos!")
        return True
    else:
        nome = input("Digite seu nome: ")
        data_nasc = input("Digite sua data de nascimento (AAAA-MM-DD): ")
        endereco = input("Digite seu endereço: ")
        request.update({'nome': nome, 'data_nasc': data_nasc, 'endereco': endereco})
        sock.sendall(json.dumps(request).encode('utf-8'))
        response = json.loads(sock.recv(4096).decode('utf-8'))
        if response == "Cadastro e login bem-sucedidos":
            print("Cadastro e login bem-sucedidos!")
            return True
        else:
            print("Falha no cadastro. Tente novamente.")
            return False

def client():
    host = os.environ.get('SERVER_HOST', 'server')
    port = int(os.environ.get('SERVER_PORT', '8082'))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    while not connected:
        try:
            sock.connect((host, port))
            connected = True
        except ConnectionRefusedError:
            print("Connection refused, retrying in 2 seconds...")
            time.sleep(2)
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
                sock.sendall(json.dumps(request).encode('utf-8'))
                response = json.loads(sock.recv(4096).decode('utf-8'))
                print("Voos disponíveis:", response)
            elif escolha == '2':
                try:
                    voo_id = int(input("Digite o ID do voo: "))
                except ValueError:
                    print("ID do voo inválido.")
                    continue
                request = {'action': 'listar_vagas', 'voo_id': voo_id}
                sock.sendall(json.dumps(request).encode('utf-8'))
                response = json.loads(sock.recv(4096).decode('utf-8'))
                print(f"Vagas disponíveis no voo {voo_id}:", response)
            elif escolha == '3':
                try:
                    voo_id = int(input("Digite o ID do voo: "))
                except ValueError:
                    print("ID do voo inválido.")
                    continue
                assento = input("Digite o número do assento: ")
                request = {'action': 'reservar_vaga', 'voo_id': voo_id, 'assento': assento}
                sock.sendall(json.dumps(request).encode('utf-8'))
                response = json.loads(sock.recv(4096).decode('utf-8'))
                print(response)
            elif escolha == '4':
                print("Saindo...")
                break
            else:
                print("Opção inválida.")
    finally:
        sock.close()

if __name__ == "__main__":
    client()
