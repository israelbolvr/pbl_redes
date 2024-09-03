class Vaga:
    def __init__(self, status, assento, voo):
        self.status = status
        self.assento = assento
        self.voo = voo

    def reservar(self):
        if self.status == 'disponivel':
            self.status = 'reservado'
            return True
        return False