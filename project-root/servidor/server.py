import socket
import pickle
import threading
from Models.Voo import Voo
from Models.Vaga import Vaga
from Models.Passageiro import Passageiro
from threading import Lock

voos = []
passageiros = []

# Locks para sincronização
voos_lock = Lock()
passageiros_lock = Lock()

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
            request = client_socket.recv(4096)
            if not request:
                break
            data = pickle.loads(request)
            action = data.get('action')

            if action == 'login':
                cpf = data.get('cpf')
                senha = data.get('senha')
                with passageiros_lock:
                    passageiro = next((p for p in passageiros if p.cpf == cpf), None)
                if passageiro:
                    if passageiro.senha == senha:
                        response = "Login bem-sucedido"
                        logged_in = True
                    else:
                        response = "Senha incorreta"
                else:
                    response = "Novo usuário"
                client_socket.send(pickle.dumps(response))

                if response == "Novo usuário":
                    nome = data.get('nome')
                    data_nasc = data.get('data_nasc')
                    endereco = data.get('endereco')
                    novo_passageiro = Passageiro(nome, cpf, data_nasc, endereco, senha)
                    with passageiros_lock:
                        passageiros.append(novo_passageiro)
                    response = "Cadastro e login bem-sucedidos"
                    logged_in = True
                    passageiro = novo_passageiro
                    client_socket.send(pickle.dumps(response))

        while True:
            request = client_socket.recv(4096)
            if not request:
                break

            data = pickle.loads(request)
            action = data.get('action')

            if action == 'listar_voos':
                with voos_lock:
                    response = [(voo.id_voo, voo.local_saida, voo.local_destino) for voo in voos]
            elif action == 'listar_vagas':
                voo_id = data.get('voo_id')
                with voos_lock:
                    voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    response = [(vaga.assento, vaga.status) for vaga in voo.listar_vagas_disponiveis()]
                else:
                    response = "Voo não encontrado"
            elif action == 'reservar_vaga':
                voo_id = data.get('voo_id')
                assento = data.get('assento')
                with voos_lock:
                    voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    vaga = next((v for v in voo.vagas if v.assento == assento), None)
                    if vaga and vaga.reservar():
                        response = f"Assento {assento} reservado com sucesso."
                    else:
                        response = "Assento indisponível ou não encontrado."
                else:
                    response = "Voo não encontrado"
            elif action == 'sair':
                response = "Desconectado"
                client_socket.send(pickle.dumps(response))
                break
            else:
                response = "Ação inválida"

            client_socket.send(pickle.dumps(response))
    except Exception as e:
        print(f"Erro ao lidar com cliente: {e}")
    finally:
        client_socket.close()

def client_thread(client_socket):
    handle_client(client_socket)

def server(host='0.0.0.0', port=8082):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Servidor rodando e aguardando conexões...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr}")
        thread = threading.Thread(target=client_thread, args=(client_socket,))
        thread.start()

server()
