import threading

class Vaga:
    def __init__(self, status, assento, voo):
        self.status = status
        self.assento = assento
        self.voo = voo
        self.lock = threading.Lock()

    def reservar(self):
        with self.lock:
            if self.status == "disponivel":
                self.status = "reservado"
                return True
            else:
                return False
