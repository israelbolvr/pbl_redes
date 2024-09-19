class Passageiro:
    def __init__(self, nome, cpf, data_nasc, endereco, senha):
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.endereco = endereco
        self.senha = senha  # hashed password
