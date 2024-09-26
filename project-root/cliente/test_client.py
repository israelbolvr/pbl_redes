import threading
import time
import random
import client  # Importa o módulo client.py existente

def simulate_client(client_id, server_ip, server_port):
    print(f"Cliente {client_id}: Iniciando simulação...")
    try:
        sock = client.connect_with_retry(server_ip, server_port)
        if sock is None:
            print(f"Cliente {client_id}: Não foi possível conectar ao servidor.")
            return

        # Simula um login ou cadastro
        cpf = f"00000000{client_id}"
        senha = "senha123"
        nome = f"Cliente {client_id}"
        request = {'action': 'login', 'cpf': cpf, 'senha': senha}
        client.send_msg(sock, request)
        response = client.recv_msg(sock)

        if response == "Senha incorreta":
            print(f"Cliente {client_id}: Senha incorreta.")
            sock.close()
            return
        elif response == "Login bem-sucedido":
            print(f"Cliente {client_id}: Login bem-sucedido!")
        elif response == "Novo usuário":
            request = {'action': 'cadastro', 'cpf': cpf, 'senha': senha, 'nome': nome}
            client.send_msg(sock, request)
            response = client.recv_msg(sock)
            if response == "Cadastro e login bem-sucedidos":
                print(f"Cliente {client_id}: Cadastro e login bem-sucedidos!")
            else:
                print(f"Cliente {client_id}: Falha no cadastro.")
                sock.close()
                return
        else:
            print(f"Cliente {client_id}: Erro desconhecido.")
            sock.close()
            return

        # Inicializa a lista de IDs de voos
        voo_ids = []

        # Realiza algumas operações aleatórias
        for index in range(3):
            if(index == 0):
                action = 'listar_voos'
            elif(index == 1):
                action = 'listar_vagas'
            elif(index == 2):
                action = 'reservar_vaga'
                
            if action == 'listar_voos':
                request = {'action': 'listar_voos'}
                client.send_msg(sock, request)
                response = client.recv_msg(sock)
                print(f"Cliente {client_id}: Voos disponíveis recebidos.")
                voo_ids = [voo[0] for voo in response]  # Armazena os IDs dos voos para uso posterior
            elif action == 'listar_vagas':
                if not voo_ids:
                    print(f"Cliente {client_id}: Nenhum voo disponível para listar vagas.")
                    continue
                voo_id = str(2)
                request = {'action': 'listar_vagas', 'voo_id': voo_id}
                client.send_msg(sock, request)
                response = client.recv_msg(sock)
                print(f"Cliente {client_id}: Vagas do voo {voo_id} recebidas.")

            elif action == 'reservar_vaga':
                if not voo_ids:
                    print(f"Cliente {client_id}: Nenhum voo disponível para reservar vaga.")
                    continue
                voo_id = voo_ids[1]
                assento = str(5)
                request = {'action': 'reservar_vaga', 'voo_id': voo_id, 'assento': assento}
                client.send_msg(sock, request)
                response = client.recv_msg(sock)
                print(f"Cliente {client_id}: {response} voo: {voo_id}")

            # Simula tempo de processamento
            time.sleep(random.uniform(0.5, 2.0))

        # Simula perda de conexão
        if random.choice([True, False]):
            print(f"Cliente {client_id}: Simulando perda de conexão.")
            sock.close()
        else:
            request = {'action': 'sair'}
            client.send_msg(sock, request)
            sock.close()
            print(f"Cliente {client_id}: Conexão encerrada normalmente.")

    except Exception as e:
        print(f"Cliente {client_id}: Erro - {e}")
        import traceback
        traceback.print_exc()



def main():
    print("Iniciando testes com clientes simultâneos...")
    num_clients = 10  # Número de clientes simultâneos
    threads = []
    server_ip = client.SERVER_IP
    server_port = client.SERVER_PORT

    for client_id in range(1, num_clients + 1):
        t = threading.Thread(target=simulate_client, args=(client_id, server_ip, server_port))
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Pequeno atraso entre as inicializações

    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()

    print("Testes concluídos.")

if __name__ == "__main__":
    main()
