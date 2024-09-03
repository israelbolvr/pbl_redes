class Voo:
    def __init__(self, id_voo, data, local_saida, local_destino):
        self.id_voo = id_voo
        self.data = data
        self.local_saida = local_saida
        self.local_destino = local_destino
        self.vagas = []

    def adicionar_vaga(self, vaga):
        self.vagas.append(vaga)

    def listar_vagas_disponiveis(self):
        return [vaga for vaga in self.vagas if vaga.status == 'disponivel']