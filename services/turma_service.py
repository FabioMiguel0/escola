from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        professor_id INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS turma_alunos (
        turma_id INTEGER,
        aluno_id INTEGER
    )
    """)
    conn.commit()
    conn.close()

def create(nome):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO turmas (nome) VALUES (?)", (nome,))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def list_turmas():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM turmas ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_turma(turma_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM turmas WHERE id=?", (turma_id,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None

def list_alunos_by_turma(turma_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.* FROM turma_alunos ta
        JOIN alunos a ON a.id = ta.aluno_id
        WHERE ta.turma_id = ?
        ORDER BY a.nome
    """, (turma_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_aluno_to_turma(turma_id: int, aluno_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO turma_alunos (turma_id, aluno_id) VALUES (?, ?)", (turma_id, aluno_id))
    conn.commit()
    conn.close()

def delete(id_):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM turmas WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def count_turmas():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) as c FROM turmas")
    r = cur.fetchone()
    conn.close()
    return r["c"] if r else 0
