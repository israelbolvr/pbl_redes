import socket
import pickle
import threading
import struct
from Models.Voo import Voo
from Models.Vaga import Vaga
from Models.Passageiro import Passageiro
from threading import Lock
import itertools
from datetime import datetime, timedelta

voos = []
passageiros = []

# Locks para sincronização
voos_lock = Lock()
passageiros_lock = Lock()

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

def mock_voos():
 #   cidades = ["Belém", "Fortaleza", "São Paulo", "Rio de Janeiro", "Salvador", "Recife"]
    cidades = ["São Paulo", "Rio de Janeiro", "Salvador" ]
    combinacoes = list(itertools.permutations(cidades, 2))
    data_inicial = datetime.now()

    voo_id = 1
    for (saida, destino) in combinacoes:
        data_voo = data_inicial + timedelta(days=voo_id)
        voo = Voo(voo_id, data_voo.strftime("%Y-%m-%d"), saida, destino)
        # Adicionar 30 assentos numerados
        for numero_assento in range(1, 11):
            vaga = Vaga("disponivel", str(numero_assento), voo)
            voo.adicionar_vaga(vaga)
        voos.append(voo)
        voo_id += 1

mock_voos()

def handle_client(client_socket):
    try:
        logged_in = False
        passageiro = None

        while not logged_in:
            data = recv_msg(client_socket)
            if not data:
                break
            action = data.get('action')

            if action == 'login:
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
                    send_msg(client_socket, response)
                else:
                    response = "Novo usuário"
                    send_msg(client_socket, response)
            elif action == 'cadastro':
                nome = data.get('nome')
                cpf = data.get('cpf')
                senha = data.get('senha')
                novo_passageiro = Passageiro(nome, cpf, senha)
                with passageiros_lock:
                    passageiros.append(novo_passageiro)
                response = "Cadastro e login bem-sucedidos"
                logged_in = True
                passageiro = novo_passageiro
                send_msg(client_socket, response)
            else:
                response = "Ação inválida durante o login"
                send_msg(client_socket, response)

        while logged_in:
            data = recv_msg(client_socket)
            if not data:
                break

            action = data.get('action')

            if action == 'listar_voos':
                with voos_lock:
                    response = [(voo.id_voo, voo.local_saida, voo.local_destino) for voo in voos]
                send_msg(client_socket, response)
            elif action == 'listar_vagas':
                voo_id = data.get('voo_id')
                with voos_lock:
                    voo = next((v for v in voos if v.id_voo == voo_id), None)
                if voo:
                    response = [(vaga.assento, vaga.status) for vaga in voo.vagas]
                else:
                    response = "Voo não encontrado"
                send_msg(client_socket, response)
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
                send_msg(client_socket, response)
            elif action == 'sair':
                response = "Desconectado"
                send_msg(client_socket, response)
                break
            else:
                response = "Ação inválida"
                send_msg(client_socket, response)
    except Exception as e:
        print(f"Erro ao lidar com cliente: {e}")
        import traceback
        traceback.print_exc()
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
