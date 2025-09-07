from models.comunicado import Comunicado
from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comunicados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        texto TEXT,
        data TEXT
    )
    """)
    conn.commit()
    conn.close()

def list_comunicados():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM comunicados ORDER BY id DESC")
    rows = cur.fetchall(); conn.close()
    return [dict(r) for r in rows]

def create(titulo, texto, data):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO comunicados (titulo, texto, data) VALUES (?, ?, ?)", (titulo, texto, data))
    conn.commit(); conn.close()

class ComunicadoService:
    def __init__(self):
        self.comunicados = []

    def enviar_comunicado(self, comunicado: Comunicado):
        self.comunicados.append(comunicado)

    def editar_comunicado(self, id_comunicado, **kwargs):
        for c in self.comunicados:
            if c.id_comunicado == id_comunicado:
                for chave, valor in kwargs.items():
                    setattr(c, chave, valor)

    def excluir_comunicado(self, id_comunicado):
        self.comunicados = [c for c in self.comunicados if c.id_comunicado != id_comunicado]

    def listar_comunicados(self):
        return self.comunicados
