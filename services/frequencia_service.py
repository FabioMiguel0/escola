from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS frequencia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turma_id INTEGER,
        aluno_id INTEGER,
        data TEXT,
        presente INTEGER -- 0/1
    )
    """)
    conn.commit()
    conn.close()

def set_presenca(turma_id: int, aluno_id: int, data: str, presente: bool):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO frequencia (turma_id, aluno_id, data, presente) VALUES (?, ?, ?, ?)
    """, (turma_id, aluno_id, data, 1 if presente else 0))
    conn.commit()
    conn.close()

def get_presencas_by_turma_date(turma_id: int, data: str):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM frequencia WHERE turma_id=? AND data=?", (turma_id, data))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_presencas_by_aluno(aluno_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM frequencia WHERE aluno_id=? ORDER BY data DESC", (aluno_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
