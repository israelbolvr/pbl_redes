import socket
import json
import threading
from Models.Voo import Voo
from Models.Vaga import Vaga
from Models.Passageiro import Passageiro
import bcrypt

voos = []
passageiros = []
global_lock = threading.Lock()  # Lock global para proteger acesso à lista de passageiros

def mock_voos():
    voo1 = Voo(1, "2024-09-15", "Belém", "Fortaleza")
    voo1.adicionar_vaga(Vaga("disponivel", "1A", voo1))
    voo1.adicionar_vaga(Vaga("disponivel", "1B", voo1))
    voos.append(voo1)

    voo2 = Voo(2, "2024-09-16", "Fortaleza", "São Paulo")
    voo2.adicionar_vaga(Vaga("disponivel", "2A", voo2))
    voo2.adicionar_vaga(Vaga("disponivel", "2B", voo2))
    voos.append(voo2)

mock_voos()

def handle_client(client_socket):
    try:
        logged_in = False
        passageiro = None

        while not logged_in:
            data = client_socket.recv(4096)
            if not data:
                break
            request = json.loads(data.decode('utf-8'))
            action = request.get('action')

            if action == 'login':
                cpf = request.get('cpf')
                senha = request.get('senha')

                # Usar o lock global para acessar a lista de passageiros
                with global_lock:
                    passageiro = next((p for p in passageiros if p.cpf == cpf), None)
                    if passageiro:
                        if bcrypt.checkpw(senha.encode('utf-8'), passageiro.senha):
                            response = "Login bem-sucedido"
                            logged_in = True
                        else:
                            response = "Senha incorreta"
                    else:
                        # Se o passageiro não existe, criar novo passageiro
                        nome = request.get('nome')
                        data_nasc = request.get('data_nasc')
                        endereco = request.get('endereco')
                        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                        novo_passageiro = Passageiro(nome, cpf, data_nasc, endereco, hashed_senha)
                        
                        # Adicionar o novo passageiro à lista com proteção de lock
                        passageiros.append(novo_passageiro)
                        response = "Cadastro e login bem-sucedidos"
                        logged_in = True
                        passageiro = novo_passageiro

                client_socket.sendall(json.dumps(response).encode('utf-8'))

        while True:
            data = client_socket.recv(4096)
            if not data:
                break

            request = json.loads(data.decode('utf-8'))
            action = request.get('action')

            if action == 'listar_voos':
                response = [(voo.id_voo, voo.local_saida, voo.local_destino) for voo in voos]
            elif action == 'listar_vagas':
                voo_id = request.get('voo_id')
                voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    response = [(vaga.assento, vaga.status) for vaga in voo.listar_vagas_disponiveis()]
                else:
                    response = "Voo não encontrado"
            elif action == 'reservar_vaga':
                voo_id = request.get('voo_id')
                assento = request.get('assento')
                voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    vaga = next((v for v in voo.vagas if v.assento == assento), None)
                    if vaga and vaga.reservar():
                        response = f"Assento {assento} reservado com sucesso."
                    else:
                        response = "Assento indisponível ou não encontrado."
                else:
                    response = "Voo não encontrado"
            else:
                response = "Ação inválida"

            client_socket.sendall(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print(f"Erro ao lidar com cliente: {e}")
    finally:
        client_socket.close()

def client_thread(client_socket):
    handle_client(client_socket)

def server():
    host = '0.0.0.0'
    port = 8082
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor rodando e aguardando conexões em {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr}")
        thread = threading.Thread(target=client_thread, args=(client_socket,))
        thread.start()

server()
