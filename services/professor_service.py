from models.professor import Professor
import sqlite3
from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def create(nome):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO professores (nome) VALUES (?)", (nome,))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def list_professores():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM professores ORDER BY nome")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete(id_):
    """Remove professor pelo id."""
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM professores WHERE id = ?", (id_,))
    conn.commit()
    conn.close()

def count_professores():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) as c FROM professores")
    r = cur.fetchone()
    conn.close()
    return r["c"] if r else 0

class ProfessorService:
    def __init__(self):
        self.professores = []

    def cadastrar_professor(self, professor: Professor):
        self.professores.append(professor)

    def editar_professor(self, id_professor, **kwargs):
        for prof in self.professores:
            if prof.id_professor == id_professor:
                for chave, valor in kwargs.items():
                    setattr(prof, chave, valor)

    def excluir_professor(self, id_professor):
        self.professores = [p for p in self.professores if p.id_professor != id_professor]

    def listar_professores(self):
        return self.professores
