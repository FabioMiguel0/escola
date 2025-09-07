from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        professor_id INTEGER
    )
    """)
    conn.commit()
    conn.close()

def add_disciplina(nome: str, professor_id: int = None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO disciplinas (nome, professor_id) VALUES (?, ?)", (nome, professor_id))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return nid

# compatibilidade: create usado por outras views
def create(nome: str, professor_id: int = None):
    return add_disciplina(nome, professor_id)

def get_disciplina(disciplina_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM disciplinas WHERE id=?", (disciplina_id,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None

def update(disciplina_id: int, nome: str = None, professor_id: int = None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE disciplinas SET nome=?, professor_id=? WHERE id=?", (nome, professor_id, disciplina_id))
    conn.commit()
    conn.close()

def delete(disciplina_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM disciplinas WHERE id=?", (disciplina_id,))
    conn.commit()
    conn.close()

def list_disciplinas():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM disciplinas ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
