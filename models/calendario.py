class Calendario:
    def __init__(self, id=None, evento="", data="", descricao=""):
        self.id = id
        self.evento = evento
        self.data = data  # formato: "YYYY-MM-DD"
        self.descricao = descricao

    def __repr__(self):
        return f"Calendario(id={self.id}, evento='{self.evento}', data='{self.data}')"
